import re

from django.apps import AppConfig
from django.conf import settings


class CalicoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calico'

    def ready(self, *args, **kwargs):
        super().ready(*args, **kwargs)

        if callable(getattr(settings, 'ANGLES', {}).get('mappers', {}).get('component')):
            self.patch_get_wrapping_tag_name()
        else:
            self.patch_parse_attributes()

    def is_patched(self, klass):
        return getattr(klass, '_patched_by_calico', False)

    def mark_patched(self, klass):
        klass._patched_by_calico = True

    def patch_parse_attributes(self):
        from dj_angles.tags import Tag

        if self.is_patched(Tag):
            return

        Tag.original_parse_attributes = Tag.parse_attributes

        def parse_attributes(self):
            self.original_parse_attributes()
            to_ignore = []
            for index, attribute in enumerate(self.attributes):
                if attribute.key.startswith('wrap:'):
                    to_ignore.append(index)

            for index in reversed(to_ignore):
                self.attributes.pop(index)

        Tag.parse_attributes = parse_attributes
        self.mark_patched(Tag)

    def patch_get_wrapping_tag_name(self):
        from dj_angles.tags import Tag

        if self.is_patched(Tag):
            return

        Tag.original_get_wrapping_tag_name = Tag.get_wrapping_tag_name
        exp = re.compile('^dj-')

        def get_wrapping_tag_name(self, *args, **kwargs):
            name = self.original_get_wrapping_tag_name(*args, **kwargs)
            return exp.sub('calico-', name)

        Tag.get_wrapping_tag_name = get_wrapping_tag_name
        self.mark_patched(Tag)


