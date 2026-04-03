from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.translation import activate
from products.models import (
    Manufacturer,
    ComicBookProduct,
    ToyProduct,
    ClothesProduct,
)


def index(request):
    """ Home page """
    comics = ComicBookProduct.objects.all()[:12]
    toys = ToyProduct.objects.all()[:12]
    clothes = ClothesProduct.objects.all()[:12]
    manufacturers = Manufacturer.objects.all()[:12]

    context = {
        'comics': comics,
        'toys': toys,
        'clothes': clothes,
        'manufacturers': manufacturers,
    }
    return render(request, 'main/index.html', context)


def about(request):
    """ About """
    return render(request, 'main/about.html')


def delivery(request):
    """ Delivery """
    return render(request, 'main/delivery.html')


def set_language(request, language_code):
    """ Set language """
    languages_dict = dict(settings.LANGUAGES)
    if languages_dict.get(language_code, None):
        activate(language_code)
    return redirect('main:index')


def set_currency(request, currency_code):
    """ Set currency """
    currencies_dict = dict(settings.CURRENCIES)
    if currencies_dict.get(currency_code, None):
        request.session['currency_code'] = currency_code
    next_page = request.META.get('HTTP_REFERER', '/')
    return redirect(next_page)


def set_city(request, city_code):
    """ Set city """
    cities_dict = dict(settings.CITIES)
    if cities_dict.get(city_code, None):
        request.session['city_code'] = city_code
    next_page = request.META.get('HTTP_REFERER', '/')
    return redirect(next_page)


def error_400(request, exception):
    """ Error 400 """
    return render(request, 'errors/400.html', status=400)


def error_403(request, exception):
    """ Error 403 """
    return render(request, 'errors/403.html', status=403)


def error_404(request, exception):
    """ Error 404 """
    return render(request, 'errors/404.html', status=404)


def error_500(request):
    """ Error 500 """
    return render(request, 'errors/500.html', status=500)
