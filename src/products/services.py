from django.conf import settings
from django.db import models
from django.utils import translation


def sort_products_by_name(queryset, reverse=False):
    """ Returns products sorted by name """
    lang_code = translation.get_language()

    if lang_code == settings.LANGUAGE_CODE:
        qs = queryset.annotate(
            name_translation=models.F('name'),
        )
    else:
        qs = queryset.filter(
            translations__language=lang_code,
        ).annotate(
            name_translation=models.F('translations__name'),
        )

    if reverse:
        qs = qs.order_by('-name_translation')
    else:
        qs = qs.order_by('name_translation')

    return qs


def get_stats_of_reviews(reviews):
    """ Returns statistics of product reviews """
    stats_of_reviews = {}

    for number in range(5, 0, -1):
        number_count = reviews.filter(rating=number).count()
        if number_count:
            number_percent = (number_count * 100) / reviews.count()
        else:
            number_percent = 0
        stats_of_reviews[str(number)] = (number_count, int(number_percent))

    return stats_of_reviews
