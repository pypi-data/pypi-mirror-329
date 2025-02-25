from datetime import timedelta, datetime

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Page


class PageSitemap(Sitemap):
    protocol = 'http' if settings.DEBUG else 'https'
    url_name = 'page'

    def is_index(self, obj):
        return obj.slug in ('index', 'fr/index', 'blog/index')

    def items(self):
        return Page.pages_in_dir(recursive=True, prune_translations=False)

    def location(self, obj):
        return reverse(self.url_name, kwargs={'slug': obj.slug})

    def lastmod(self, obj):
        return obj.lastmod

    def priority(self, obj):

        if self.lastmod(obj) < datetime.now() - timedelta(days=7) and \
                obj.slug.rsplit('/', 1)[-1] not in ('credits', 'legal-notice', 'mentions-legales'):
            return 1

        if self.is_index(obj):
            return .75

        return .2

    def changefreq(self, obj):
        return 'weekly' if self.is_index(obj) else 'monthly'


sitemaps = {
    'sitemaps': {
        'pages': PageSitemap,
    },
}
