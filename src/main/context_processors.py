from django.conf import settings


def main_context(request):
    context = {
        'SITE_NAME': settings.SITE_NAME,
        'CURRENCIES': settings.CURRENCIES,
        'СITIES': settings.CITIES,
    }

    currency_code = request.session.get('currency_code')
    for currency in settings.CURRENCIES:
        if currency[0] == currency_code:
            context['user_currency'] = currency

    city_code = request.session.get('city_code')
    for city in settings.CITIES:
        if city[0] == city_code:
            context['user_city'] = city[1]

    return context
