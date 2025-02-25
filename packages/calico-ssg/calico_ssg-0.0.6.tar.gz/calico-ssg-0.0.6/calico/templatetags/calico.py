import os

from django import template
from django.template import Template, Context
from django.utils.text import capfirst, slugify

from dj_angles.settings import get_setting
from markdown_deux.templatetags.markdown_deux_tags import markdown_filter
from yak.component import Komponent
from yak.tags import InclusionNode, TemplateTag

from ..exceptions import PageDoesNotExist
from ..favicon import FavIcon
from ..models import Site
from ..thumbnailer import Thumbnailer
from ..utils import calico_setting, blog_posts_per_author, date_from_str_func, get_tags, get_author


try:
    from dj_angles.regex_replacer import convert_template
except ImportError:
    # dj-angles < 0.14
    from dj_angles.regex_replacer import replace_django_template_tags as convert_template

register = template.Library()


class Calico(Komponent):
    node_class = InclusionNode

    def __call__(self, parser, token):
        rv = super().__call__(parser, token)
        self.node.template_base = get_setting('component_folder', False)
        return rv


register.tag(Calico.as_tag())


@register.filter
def path_join(slug, prefix):
    if prefix and prefix != '':
        return '/'.join([prefix, slug])
    return slug


@register.filter
def load_items(items_list, page):
    if items_list is None:
        return []
    return page.get_sub_items(items_list)


@register.filter
def translations(page):
    return [
        (f'/{pre}/' if pre else '/', lang)
        for pre, lang in calico_setting('LANGUAGES')
        if pre != page.language
    ]


@register.filter
def is_index(slug):
    return slug == 'index' or slug.endswith('/index')


@register.filter
def date_from_str(date_str):
    return date_from_str_func(date_str)


@register.filter
def author_details(author_slug):
    try:
        post = get_author(author_slug)
    except PageDoesNotExist:
        return {
            'name': capfirst(author_slug),
            'title': capfirst(author_slug),
        }

    rv = post.metadata
    if 'name' not in rv:
        rv['name'] = rv.get('title', capfirst(author_slug))
    rv['content'] = post.md_content
    return rv


@register.filter
def author_link(author_slug):
    return f'/{calico_setting("BLOG_AUTHOR_DIR")}/{author_slug}.html'


@register.filter
def tags(author_slug):
    tags = Site().get_tags(author_slug)
    rv = [(t[0], [post.meta.data for post in t[1]]) for t in tags]
    return rv


@register.filter
def authored(author_slug):
    return [post.meta.data for post in Site().get_posts(author_slug)]


@register.filter
def tag_link(tag):
    return f'/{calico_setting("TAGS_PAGE")}.html?tag={slugify(tag)}'


@register.filter
def items(dictionary):
    return dictionary.items()


@register.filter
def background_img(image_path, divide_by=1):
    tn = Thumbnailer(image_path, divide_by=divide_by)
    return tn.bg_img()


@register.filter
def section_or_obj_background(section, obj):
    if section.get('use_image', False) and obj.metadata.get('image', False):
        return obj.metadata['image']
    return section.get('background', False)


@register.filter
def md_include(content, style='default'):
    context = Context()
    html = markdown_filter(content, style=style)
    return Template(convert_template(html)).render(context)


@register.filter
def collection_top(item, collection=None):
    return Site().get_collection(
        collection or item.metadata['collection'],
        sort_by=item.metadata.get('collection_sort_by', 'slug'),
        count=int(item.metadata.get('top_count', 0))
    )


@register.filter
def collection_grouped_top(item):
    return Site().get_collection(
        item.metadata['collection'],
        sort_by=item.metadata.get('collection_sort_by', 'slug'),
        group_by=item.metadata['group_by'],
        count=int(item.metadata.get('top_count', 0))
    )


class FavIconTag(TemplateTag):
    template_name = 'calico/favicon.html'

    def render(self, svg_path, image_path, include_manifest=False):
        fav = FavIcon(svg_path, image_path)
        return {
            'favicon': fav,
            'include_manifest': include_manifest,
        }


class SourceSet(TemplateTag):
    template_name = 'calico/sourceset.html'

    def render(self, image_path, divide_by=1, **kwargs):
        tn = Thumbnailer(image_path, divide_by=divide_by)
        return {
            'original': tn.max_res or tn.original_url,
            'sizes': tn.sizes,
            'srcset': tn.srcset,
            **kwargs
        }


class Var(TemplateTag):
    allow_as = False

    def render(self, context, **kwargs):
        for key, val in kwargs.items():
            context[key] = val
        return ''


register.tag('favicon', FavIconTag.as_tag())
register.tag(SourceSet.as_tag())
register.tag(Var.as_tag())
