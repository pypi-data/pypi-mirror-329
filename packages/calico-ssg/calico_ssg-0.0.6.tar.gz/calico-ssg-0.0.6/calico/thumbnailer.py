from collections import namedtuple
import os
from pathlib import Path
from PIL import Image

from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.utils.text import slugify

from .utils import calico_setting


Thumbnail = namedtuple('Thumbnail', ['size', 'adjusted_size', 'url'])


class Thumbnailer:

    def __init__(self, filename, divide_by=1):
        self.original_url = filename
        self.original = finders.find(filename)
        self.max_res = None

        if self.original is None:
            raise ValueError(f'Unable to find {filename}')

        self.thumb_dir = os.path.join(Path(self.original).parent, calico_setting('THUMBS_SUBDIR'))
        if not os.path.isdir(self.thumb_dir):
            os.mkdir(self.thumb_dir)

        self._base, self._ext = (self.original.rsplit('/', 1)[-1]).rsplit('.', 1)

        image = Image.open(self.original)
        self.original_size = image.size

        self.thumbs = []
        for name, size in calico_setting('THUMBS').items():
            if size is None:
                target_filename = f'{self._base}.{self.original_size[0]:.0f}x{self.original_size[1]:.0f}.webp'
            else:
                adjusted_size = tuple(s / divide_by for s in size) if size is not None else None
                target_filename = f'{self._base}.{adjusted_size[0]:.0f}x{adjusted_size[1]:.0f}.webp'

            if size is not None and all([adjusted_size[i] >= image.size[i] for i in range(2)]):
                continue

            target_name = os.path.join(self.thumb_dir, target_filename)
            if not os.path.isfile(target_name) or os.path.getctime(target_name) < os.path.getmtime(self.original):
                tn = image.copy().convert("RGB")
                if size is not None:
                    tn.thumbnail(adjusted_size)
                tn.save(target_name, 'WEBP')

            url = os.path.join(
                self.original_url.rsplit('/', 1)[0],
                calico_setting('THUMBS_SUBDIR'),
                target_filename
            )
            if size is None:
                self.max_res = url
            else:
                self.thumbs.append(Thumbnail(size, adjusted_size, url))

    def media(self, thumbnail, include_lower=False):
        rv = f'(max-width: {thumbnail.size[0]:.0f}px)'

        if include_lower:
            size = 0
            try:
                size = max([t.size[0] for t in self.thumbs if t.size[0] < thumbnail.size[0]]) + 1
            except ValueError:
                pass

            if size > 0:
                rv = f'{rv} and (min-width: {size:.0f}px)'

        return rv

    @property
    def sizes(self):
        return ', '.join([
            f'() {t.adjusted_size[0]:.0f}'
            for t in self.thumbs
        ] + [
            f'(min-width: {(max([t.size[0] for t in self.thumbs]) + 1):.0f}px) {self.original_size[0]:.0f}',
        ])

    @property
    def srcset(self):
        return ', '.join([
            f'{static(t.url)} {t.adjusted_size[0]:.0f}w'
            for t in self.thumbs
        ])

    def bg_img(self, id=None):
        if id is None:
            id = slugify(self.original_url)
        return '\n'.join([
            f'#{id} {{background-image: url({static(self.max_res or self.original_url)});}}'
        ] + [
            f'@media {self.media(t, include_lower=True)} {{ #{id} {{background-image: url({static(t.url)}); }} }}'
            for t in self.thumbs
        ])

