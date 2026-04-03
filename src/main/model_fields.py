from django.conf import settings
from django.utils import translation


class TranslatedField(object):
    """ Translated Field """

    def __init__(self, field_name):
        self.field_name = field_name

    def __get__(self, instance, owner):
        lang_code = translation.get_language()
        if lang_code == settings.LANGUAGE_CODE:
            return getattr(instance, self.field_name)
        else:
            translations = instance.translations.filter(
                language=lang_code,
            ).first() or instance
            return getattr(translations, self.field_name)
