from django.urls.converters import SlugConverter


class PagePathConverter(SlugConverter):
    regex = "[-a-zA-Z0-9_/]+"
