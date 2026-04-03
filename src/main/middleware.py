from django.conf import settings


class SetCurrencyMiddleware:
    """ Set currency in session """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'currency_code' not in request.session:
            if request.LANGUAGE_CODE == 'en':
                request.session['currency_code'] = settings.CURRENCIES[0][0]
            elif request.LANGUAGE_CODE == 'ru':
                request.session['currency_code'] = settings.CURRENCIES[2][0]
            elif request.LANGUAGE_CODE == 'be':
                request.session['currency_code'] = settings.CURRENCIES[3][0]

        response = self.get_response(request)

        return response


class SetCityMiddleware:
    """ Set city in session """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'city_code' not in request.session:
            request.session['city_code'] = settings.CITIES[0][0]

        response = self.get_response(request)

        return response
