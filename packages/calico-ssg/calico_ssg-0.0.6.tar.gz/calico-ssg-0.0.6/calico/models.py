from collections import defaultdict
from datetime import datetime
from glob import glob
import os
from pathlib import Path
import warnings

from django.conf import settings
from django.urls import reverse
from django.utils.functional import classproperty, cached_property
from django.utils.html import strip_tags
from django.utils.text import capfirst

import frontmatter
from markdown2 import Markdown
import readtime
import yaml

from .exceptions import PageDoesNotExist
from .utils import calico_setting, date_from_str_func, unique_extend, Extractor, Singleton


class Page(metaclass=Singleton):

    data_file_path = None
    slug = None
    _is_single_file = False

    MDATA_DEFAULTS = {
        'title': lambda self, _: capfirst(self.slug.rsplit('/')[-1]),
    }

    @classproperty
    def base_path(cls):
        return calico_setting('CONTENT_DIR')

    @classproperty
    def pages_at_root(cls):
        return cls.pages_in_dir()

    @cached_property
    def data_dir_path(self):
        return Path(self.data_file_path).parent

    @cached_property
    def content(self):
        return self.get_files()

    @cached_property
    def md_content(self):
        return '\n\n'.join([part.content for part in self.content])

    @cached_property
    def containing_dir(self):
        containing_dir = Path(self.data_file_path).parent

        if self._is_single_file:
            return containing_dir

        return containing_dir.parent

    @cached_property
    def anchors(self):
        return {
            s['anchor']: s['title']
            for s in self.content
            if s.get('anchor', None) is not None and s.get('title', None) is not None
        }

    @property
    def lastmod(self):
        files = self.get_file_paths()

        if self._is_single_file:
            files.append(self.data_file_path)

        mtimes = [
            datetime.fromtimestamp(Path(f).stat().st_mtime)
            for f in files
        ]
        return max(mtimes)

    @cached_property
    def meta_description(self):
        if 'description' in self.metadata:
            return self.metadata['description']

        if 'excerpt' in self.metadata:
            return strip_tags(Markdown().convert(self.metadata['excerpt'])).replace('"', '').replace('\n', ' ').strip()

        return None

    @cached_property
    def language(self):
        prefix = self.slug.split('/', 1)[0]

        if prefix in [lang for lang, _ in calico_setting('LANGUAGES')]:
            return prefix

        return ''

    @cached_property
    def meta_lang(self):
        if 'lang' in self.metadata:
            return self.metadata['lang']

        lang = self.language
        if lang in ['', None]:
            lang = getattr(settings, 'LANGUAGE_CODE', None)

        return lang

    @cached_property
    def components(self):
        components = {}
        for component in calico_setting('CONTENT_COMPONENTS'):
            location = self.metadata.get(component, f'_{component}')
            if location:
                component_directory = None
                directory = self.data_dir_path

                while component_directory is None and directory != Path(self.base_path).parent:
                    loc_dir = os.path.join(directory, location)
                    if os.path.isdir(loc_dir):
                        component_directory = loc_dir
                        break

                    directory = Path(directory).parent

                if component_directory is not None:
                    components[component] = self.get_files(component_directory)

        return components

    @cached_property
    def siblings(self):
        return [p
                for p in self.pages_in_dir(directory=self.containing_dir)
                if p.slug != self.slug]

    @cached_property
    def current_root_without_me(self):
        return [p
                for p in self.pages_at_lang_root(self.language)
                if p.slug != self.slug]

    @cached_property
    def url(self):
        return reverse('page', kwargs={'slug': self.slug})

    @cached_property
    def published_at(self):
        if 'published_at' not in self.metadata:
            return self.lastmod
        else:
            return date_from_str_func(self.metadata['published_at'])

    @cached_property
    def readtime(self):
        return readtime.of_markdown(self.md_content)

    @cached_property
    def related(self):
        rv = []
        rv.extend(
            Page(item)
            for item in self.meta.data.get('related', [])
        )
        rv.extend(
            p
            for p in self.pages_in_dir(recursive=True)
            if self.slug in p.meta.data.get('related', [])
        )
        return set(rv)

    def __init__(self, slug, data_file_path=None):
        path = os.path.join(self.base_path, slug.replace('/', os.path.sep))
        self.slug = slug

        if data_file_path is not None:
            self.data_file_path = data_file_path

        if self.data_file_path is None and os.path.isdir(path):
            data_file_path = os.path.join(path, 'data.yml')
            if os.path.isfile(data_file_path):
                self.data_file_path = data_file_path
                self._is_single_file = False

        md_path = f'{path}.md'
        if self.data_file_path is None and os.path.isfile(md_path):
            self.data_file_path = md_path
            self._is_single_file = True

        if self.data_file_path is None:
            raise PageDoesNotExist(slug)

        self.meta = Extractor(self)

    @property
    def metadata(self):
        warnings.warn(
            'Accessing `Page.metadata` directly is deprecated, please use `Page.meta` insetad',
            DeprecationWarning
        )
        return self.meta.data

    def __str__(self):
        return f'Page at {self.slug}'

    def __repr__(self):
        return self.__str__()

    @classmethod
    def pages_at_lang_root(cls, lang=''):
        if lang in ['', None]:
            return cls.pages_at_root

        if lang not in [l for l, _ in calico_setting('LANGUAGES')]:
            raise ValueError(f'"{lang}" is not a know language ({calico_setting("LANGUAGES")})')

        return cls.pages_in_dir(subdir=lang)

    @classmethod
    def abs_path_to_rel_path(cls, path):
        path = f'{path}'
        if not path.startswith(cls.base_path):
            raise ValueError(f'"{path}" not in base_path ({cls.base_path}))')

        return path[len(cls.base_path) + 1:]

    @classmethod
    def abs_path_to_slug(cls, path):
        rel_path = cls.abs_path_to_rel_path(path)

        if rel_path.endswith('.md'):
            split_char = '.'
        else:
            split_char = os.path.sep

        return rel_path.rsplit(split_char, 1)[0]

    @classmethod
    def _get_abs_path_candidates(cls, path, *expr, recursive=False):
        rv = [os.path.join(path, candidate)
              for candidate in glob(os.path.join(path, *expr), recursive=recursive)]
        return rv

    @classmethod
    def get_filters(cls, cur_lang, **kwargs):
        filters = []

        if kwargs.get('prune_translations', True):
            filters.append(
                lambda p: p.language not in [lang for lang, _ in calico_setting('LANGUAGES') if lang != cur_lang]
            )

        if not kwargs.get('include_hidden', False):
            filters.append(lambda p: not any([pt[0] in ['.', '_'] for pt in p.slug.split('/')]))

        for key in ('draft', 'archive', 'unlisted'):
            if not kwargs.get(f'include_{key}', False):
                # Hack: `k=key` is used to bind the value of key
                # the left side of : in a lambda is evaluated at creation
                # the right side at execution
                # if key was used inside the lambda, it would always be the last value in the forloop
                filters.append(lambda p, k=key: not p.metadata.get(k, False))

        return filters

    @property
    def is_hidden(self):
        return any([pt[0] in ['.', '_'] for pt in self.slug.split('/')])

    @classmethod
    def pages_in_dir(cls, directory=None, subdir=None, recursive=False, **kwargs):
        cur_lang = ''

        if subdir is not None:
            if directory is None:
                directory = cls.base_path
            directory = os.path.join(directory, subdir)

        if directory is None:
            directory = cls.base_path
        else:
            rel_path = cls.abs_path_to_rel_path(directory)
            for lang, _ in calico_setting('LANGUAGES'):
                if rel_path.split(os.path.sep, 1)[0] != lang:
                    continue

                cur_lang = lang
                break

        ext_candidates = cls._get_abs_path_candidates(directory, '*', 'data.yml')
        md_candidates = cls._get_abs_path_candidates(directory, '*.md')

        if recursive:
            unique_extend(ext_candidates, cls._get_abs_path_candidates(directory, '**', '*', 'data.yml', recursive=True))
            unique_extend(md_candidates, cls._get_abs_path_candidates(directory, '**', '*.md', recursive=True))
        else:
            # sub-structures with an index pages are considered siblings of pages at the level below
            unique_extend(ext_candidates, cls._get_abs_path_candidates(directory, '*', 'index', 'data.yml'))
            unique_extend(md_candidates, cls._get_abs_path_candidates(directory, '*', 'index.md'))

        pages = [Page(cls.abs_path_to_slug(candidate))
                 for candidate in ext_candidates]

        ext_paths = [p.data_dir_path for p in pages]

        pages.extend([Page(cls.abs_path_to_slug(candidate))
                      for candidate in md_candidates
                      if Path(candidate).parent not in ext_paths])

        filters = cls.get_filters(cur_lang, **kwargs)

        return sorted([p
                       for p in pages
                       if all([f(p) for f in filters])],
                      key=lambda p: f"{p.metadata.get('weight', 999):03d}")

    def get_file_paths(self, directory=None, only=None):
        if self._is_single_file and directory is None:
            return [self.data_file_path]

        if directory is None:
            directory = self.data_dir_path

        return sorted([
            os.path.join(directory, f) for f in os.listdir(directory)
            if not os.path.isdir(os.path.join(directory, f))
            and f.endswith('.md')
            and (
                (only is None and not f.startswith('.') and not f.startswith('_'))
                or
                (only is not None and f in only)
            )
        ])

    def get_files(self, directory=None, only=None):
        files = self.get_file_paths(directory=directory, only=only)

        return sorted([
            frontmatter.load(f) for f in files
        ], key=lambda fm: f"{fm.get('weight', 999):03d}")

    def get_sub_items(self, item_slugs):
        return [frontmatter.load(os.path.join(self.data_dir_path, f'{item}.md'))
                for item in item_slugs]

    def get_metadata(self):
        data = {}
        site_yml = os.path.join(self.base_path, 'site.yml')
        if os.path.isfile(site_yml):
            data.update(yaml.safe_load(open(site_yml)))
        if self._is_single_file:
            meta = self.get_files()[0].metadata
        else:
            meta = yaml.safe_load(open(self.data_file_path))

        if meta is not None:
            data.update(meta)

        for key, func in self.MDATA_DEFAULTS.items():
            if key not in data:
                data[key] = func(self, data)

        return data


class Site(metaclass=Singleton):

    _collections = defaultdict(list)
    _posts = list()
    _pages = dict()
    _tags = defaultdict(list)

    def __init__(self):
        for page in Page.pages_in_dir(include_hidden=True, include_unlisted=True, include_archive=True, recursive=True):
            self._pages[page.slug] = page

            if page.meta.get('unlisted') or page.meta.get('archive') or page.meta.get('draft'):
                continue

            if page.is_hidden:
                if collections := page.meta.get('member_of'):
                    if isinstance(collections, str):
                        self._collections[collections].append(page)
                    else:
                        for collection in collections:
                            self._collections[collection].append(page)
                continue

            if page.meta.get('widget', '') in ('blog_post', 'blog.post'):
                page.meta.data['published_date'] = page.published_at
                page.meta.data['url'] = page.url
                page.meta.data['content'] = page.md_content
                page.meta.data['readtime'] = page.readtime

                self._posts.append(page)

                for tag in page.meta.get('tags', list()):
                    self._tags[tag].append(page)

    def get_collection(self, collection, sort_by='slug', count=0, group_by=None):

        print(collection, len(self._collections.keys()), self._collections[collection])

        if sort_by[0] == '-':
            rev = True
            sort_by = sort_by[1:]
        else:
            rev = False

        rv = sorted(
            self._collections[collection],
            key=lambda x: str(x.meta.get(sort_by)),
            reverse=rev
        )

        if count:
            rv = list(rv)[:count]

        if group_by:
            grouped = defaultdict(list)

            for item in rv:
                grouped[item.meta.get(group_by)].append(item)

            return grouped.items()

        return rv

    def _filter_posts_per_author(self, posts, author_slug):
        return [p for p in posts if author_slug == slugify(p.meta.get('author', ''))]

    def get_posts(self, author_slug=None, tag=None):
        posts = self._posts

        if tag:
            posts = self._tags[tag]

        if author_slug:
            posts = self._filter_posts_per_author(posts, author_slug)

        return sorted(posts, key=lambda p: str(p.meta.get('published_date')), reverse=True)

    def get_tags(self, author_slug=None):
        tags = self._tags

        if author_slug:
            tags = defaultdict(list)

            for tag, posts in self._tags:
                tags[tag] = self._filter_posts_per_author(posts, author_slug)

        return sorted(tags.items(), key=lambda x: -len(x[1]))
