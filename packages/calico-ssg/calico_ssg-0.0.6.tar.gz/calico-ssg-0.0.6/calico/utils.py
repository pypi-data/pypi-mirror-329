from collections import defaultdict
from datetime import datetime, date
import os

from django.conf import settings
from django.utils.text import slugify


S_DEFAULTS = {
    'BLOG_AUTHOR_DIR': 'blog/author',
    'BLOG_DIR': 'blog',
    'CONTENT_COMPONENTS': ['header', 'footer'],
    'CONTENT_DIR': os.path.join(settings.BASE_DIR, 'content'),
    'CSS_URLS': [
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css',
    ],
    'DATE_FORMATS': ('%Y-%m-%d %H:%M', '%Y-%m-%d'),
    'FORCE_HTTP': False,
    'FORCE_HTTPS': True,
    'HOST': 'localhost',
    'JS_URLS': [
        'https://cdn.jsdelivr.net/npm/alpinejs@3.14.1/dist/cdn.min.js',
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js',
    ],
    'LANGUAGES': [],
    'RSS_CONTENT': 'partial',
    'RSS_WORDS': 80,
    'TAGS_PAGE': 'blog/tags',
    'THUMBS': {
        'xs': (576, 576),
        'sm': (767, 767),
        'md': (991, 991),
        'lg': (1200, 768),
        'xl': (1400, 900),
        'xxl': (1920, 1080),
        'xxxl': None,
    },
    'THUMBS_SUBDIR': '_resized',
}


def calico_setting(key):
    return getattr(settings, f'CALICO_{key}', S_DEFAULTS.get(key, None))


def date_from_str_func(date_str):
    for fmat in calico_setting('DATE_FORMATS'):
        if isinstance(date_str, date):
            return date_str

        if isinstance(date_str, datetime):
            return date_str.date

        try:
            return datetime.strptime(date_str, fmat)
        except ValueError:
            continue


def blog_posts_per_author(author_slug):
    from .models import Page

    subdir = calico_setting('BLOG_DIR')
    posts = []

    if author_slug:
        slug = slugify(author_slug)
    else:
        slug = None

    for post in Page.pages_in_dir(subdir=subdir):
        if post.metadata.get('widget', '') not in ('blog_post', 'blog.post'):
            continue
        if slug and slug != slugify(post.metadata.get('author', '')):
            continue
        post.metadata['published_date'] = post.published_at
        post.metadata['url'] = post.url
        posts.append(post)
    return reversed(sorted(posts, key=lambda x: str(x.metadata['published_date'])))


def get_tags(author_slug):
    from .models import Page

    subdir = calico_setting('BLOG_DIR')
    tags = defaultdict(list)
    for post in Page.pages_in_dir(subdir=subdir):
        post.metadata['published_date'] = post.published_at
        post.metadata['url'] = post.url
        if 'tags' in post.metadata and (not author_slug or author_slug == post.metadata.get('author', None)):
            for tag in post.metadata['tags']:
                tags[tag].append(post)
    return sorted(tags.items(), key=lambda x: -len(x[1]))


def get_author(author_slug):
    from .models import Page

    return Page(os.path.join(calico_setting('BLOG_AUTHOR_DIR'), author_slug))


def unique_extend(orig, lst):
    orig.extend([
        p
        for p in lst
        if p not in orig
    ])


class Singleton(type):
    _instances = {}  # intentionaelly mutable

    def __call__(cls, *args, **kwargs):
        kwhash = tuple(kwargs.items())
        ahash = tuple(args)
        instance = cls._instances.get((cls, ahash, kwhash))

        if settings.DEBUG or not instance:
            instance = super().__call__(*args, **kwargs)
            cls._instances[(cls, ahash, kwhash)] = instance


        return instance


class Extractor(metaclass=Singleton):

    def __init__(self, page):
        self.page = page
        self.data = page.get_metadata()

    def __getattr__(self, prop):
        rv = self.data[prop] if prop in self.data else getattr(self.page, prop)

        if isinstance(rv, str) and rv.startswith('_'):
            method, *args = rv.split('::')
            return getattr(self, f'extract{method}')(*args)

        return rv

    def get(self, prop, default=None):
        try:
            return getattr(self, prop)
        except AttributeError:
            return default

    def extract_dir(self, index=0):
        *page_path, file = self.page.slug.split('/')
        if index >= len(page_path):
            return None
        return page_path[-1 - index]
