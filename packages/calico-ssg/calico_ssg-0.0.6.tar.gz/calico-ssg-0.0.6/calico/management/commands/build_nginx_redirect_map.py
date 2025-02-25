from django.core.management.base import BaseCommand

from ...models import Page


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--destfile', default='dist/redirect.map')

    def handle(self, *args, **options):
        pages = Page.pages_in_dir(recursive=True, prune_translations=False, include_draft=True,
                                  include_hidden=True, include_archive=True)

        with open(options['destfile'], 'w') as f:
            for page in pages:
                if not page.metadata.get('widget', None) == 'redirect':
                    continue

                f.write(f'{page.url} {page.metadata.get("url", "/__404__.html")};\n')
