"""
URL configuration for levit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django import test
from django.urls import path, register_converter
from django.utils.text import slugify

from django_distill import distill_path

from .converters import PagePathConverter
from .feeds import GeneralFeed, TagFeed
from .models import Page
from .sitemaps import sitemaps
from .utils import get_tags, calico_setting
from .views import PageView, SilentIndexView


## Start monkey patching for distill
def init(self, *args, **kwargs):
    if settings.DEBUG:
        first_host = 'localhost'
    else:
        first_host = calico_setting('HOST')

    kwargs['SERVER_NAME'] = first_host
    return self._old_init(*args, **kwargs)


test.RequestFactory._old_init = test.RequestFactory.__init__
test.RequestFactory.__init__ = init
## End monkey patching

register_converter(PagePathConverter, 'page')

urlpatterns = [
    distill_path('__404__.html', PageView.as_view(is_error_page=True), {'slug': '__404__'}, name='404',
                 distill_func=lambda: None, distill_file='__404__.html'),
    distill_path('sitemap.xml', sitemap, sitemaps, name='sitemap',
                 distill_func=lambda: [sitemaps]),
]

urlpatterns += [
    distill_path('<page:slug>.html', PageView.as_view(), name='page',
                 distill_func=lambda: [{'slug': p.slug} for p in Page.pages_in_dir(
                     recursive=True,
                     include_draft=True,
                     include_archive=True,
                     include_unlisted=True,
                     prune_translations=False)]),
    distill_path(f'{calico_setting("FEEDS_BASE")}/_rss.xml', GeneralFeed(), name='general_feed',
                 distill_func=lambda: None, distill_file=f'{calico_setting("FEEDS_BASE")}/_rss.xml'),
    distill_path(f'{calico_setting("FEEDS_BASE")}/<slug:tag>.xml', TagFeed(), name='tag_feed',
                 distill_func=lambda: [slugify(t[0]) for t in get_tags(None)]),
    path('', SilentIndexView.as_view(), name='index'),
    path('<page:slug>/', SilentIndexView.as_view(), name='dir_index'),
]
