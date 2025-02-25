from glob import glob
import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--dirname', default='templates/widgets')
        parser.add_argument('--target', default='levit/static_src/scss/_widgets.scss')

    def handle(self, *args, **options):

        scss_imports = []

        glob_base = os.path.join('*', options['dirname'])
        target_path = os.path.join(settings.BASE_DIR, options['target'])

        for filename in glob(os.path.join(glob_base, '*.scss')) + glob(os.path.join(glob_base, '**', '*.scss')):
            full_path = os.path.join(settings.BASE_DIR, filename)
            path, file = full_path.rsplit(os.path.sep, 1)
            if file.startswith('_'):
                file_base = file[1:-5]
            else:
                file_base = file[:-5]
            html_file = os.path.join(path, f'{file_base}.html')
            if os.path.isfile(html_file):
                scss_imports.append(os.path.join(
                    os.path.relpath(
                        path,
                        target_path.rsplit(os.path.sep, 1)[0]
                    ),
                    file_base
                ))

        with open(target_path, 'w') as f:
            for name in scss_imports:
                f.write(f'@import "{name}";\n')
