from decimal import Decimal
import requests
from django.conf import settings
from django.core.cache import caches


API_URL = f'https://v6.exchangerate-api.com/v6/{ settings.EXCHANGERATE_API_KEY }/pair/USD/'


def get_currency(currency_code):
    """ Returns the currency value and save it in the cache """
    currencies_cache = caches['currencies']
    cur_value = currencies_cache.get(currency_code)

    if cur_value is None:
        resp = requests.get(f'{ API_URL }{ currency_code }')
        data = resp.json()
        cur_value = data['conversion_rate']
        currencies_cache.set(currency_code, cur_value)

    return cur_value


def get_value_in_currency(value, currency_code):
    """ Returns value in currency """
    if currency_code == 'USD':
        return value
    else:
        cur_value = get_currency(currency_code)
        return round(value * Decimal(cur_value), 2)


def get_price_range_from_currency(f_min_price, f_max_price, currency_code):
    """ Returns price range from currency """
    if currency_code == 'USD':
        return (f_min_price, f_max_price)
    else:
        cur_value = get_currency(currency_code)
        min_price = f_min_price / Decimal(cur_value)
        max_price = f_max_price / Decimal(cur_value)
        return (min_price, max_price)
