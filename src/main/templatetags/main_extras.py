from django import template
from main.services import get_value_in_currency


register = template.Library()


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    """
    Returns the URL-encoded querystring for the current page,
    updating the params with the key/value pairs passed to the tag.
    """
    query = context['request'].GET.copy()
    for key, value in kwargs.items():
        query[key] = value
    return f'?{ query.urlencode() }'


@register.filter
def decimal_fractional_currency(value, currency_code):
    """ Returns the decimal and fractional parts in currency """
    value = get_value_in_currency(value, currency_code)
    return str(value).split('.')
