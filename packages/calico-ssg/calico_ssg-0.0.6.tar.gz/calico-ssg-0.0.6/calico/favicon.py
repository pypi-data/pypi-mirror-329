import os

from PIL import Image

from django.contrib.staticfiles import finders


class FavIcon:

    ICO = 'favicon.ico'
    PNG = 'favicon-{size}.png'
    DIR = '_ico'

    _sizes = (16, 32, 48, 64)
    _manifest_sizes = (192, 512, None)

    def __init__(self, svg, img):
        self.source = finders.find(img)
        self.svg_url = svg
        self.url_base = img.rsplit(os.sep, 1)[0] if img else None

        self.png = {}
        if img is not None:
            image = Image.open(self.source)
            base = self.source.rsplit(os.sep, 1)[0]

            ico_dir = os.path.join(base, self.DIR)
            if not os.path.isdir(ico_dir):
                os.mkdir(ico_dir)

            for size in (180, 192, 512):
                self.png[size] = os.path.join(base, self.DIR, self.PNG.format(size=size))
                if not os.path.isfile(self.png[size]) or \
                        os.path.getctime(self.png[size]) < os.path.getmtime(self.source):
                    png = image.copy().resize((size, size))
                    png.save(self.png[size])

            self.png[None] = self.png[512]

            self.ico = os.path.join(base, self.DIR, self.ICO)
            if not os.path.isfile(self.ico) or \
                    os.path.getctime(self.ico) < os.path.getmtime(self.source):
                ico = image.copy()
                ico.save(self.ico, sizes=[(s, s) for s in self._sizes])
        else:
            self.ico = None

    @property
    def ico_url(self):
        if self.ico:
            return os.path.join(self.url_base, self.DIR, self.ICO)
        return None

    @property
    def png_url(self):
        if 180 in self.png:
            return os.path.join(self.url_base, self.DIR, self.PNG.format(size=180))
        return None

    @property
    def png_urls(self):
        return {
            size: os.path.join(self.url_base, self.DIR, self.PNG.format(size=size))
            for size in self._manifest_sizes
            if size in self.png
        }

    @property
    def sizes(self):
        return ' '.join(f'{s}x{s}' for s in self._sizes)
