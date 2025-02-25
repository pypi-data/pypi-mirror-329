from django.http import Http404
from django.urls import reverse
from django.views.generic import DetailView, View, RedirectView, TemplateView

from .exceptions import PageDoesNotExist
from .favicon import FavIcon
from .models import Page
from .utils import calico_setting


class CalicoViewMixin(View):

    __tunables = tuple()

    def tune_args(self, kwargs):
        for arg in self.__tunables:
            setattr(self, arg, kwargs.pop(arg, getattr(self, arg)))
        return kwargs

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **self.tune_args(kwargs))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **self.tune_args(kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stylesheets'] = calico_setting('CSS_URLS')
        context['javascripts'] = calico_setting('JS_URLS')
        context['feeds_base'] = calico_setting('FEEDS_BASE')
        return context


class PageView(CalicoViewMixin, DetailView):

    __tunables = ('is_error_page', )

    template_name = 'calico/page.html'
    is_error_page = False

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')

        if slug.rsplit('/', 1)[-1].startswith('_') and not self.is_error_page:
            raise Http404

        try:
            self.object = Page(slug)
        except PageDoesNotExist:
            raise Http404

        return self.object


class SilentIndexView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        og_slug = kwargs.get('slug', '')
        if og_slug in ['', None]:
            slug = 'index'
        else:
            slug = og_slug + '/index'
        return reverse('page', kwargs={'slug': slug})


class ManifestView(TemplateView):
    template_name = 'calico/manifest.webmanifest'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p = Page('index')
        fav = FavIcon(None, p.metadata.get('favicon_img'))
        context['icons'] = fav.png_urls
        return context
