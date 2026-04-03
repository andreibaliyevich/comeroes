from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from main.services import get_value_in_currency
from products.models import Product
from coupons.forms import CouponApllyForm
from .cart import Cart


def cart_detail(request):
    """ Cart Detail """
    coupon_aplly_form = CouponApllyForm()

    context = {
        'coupon_aplly_form': coupon_aplly_form,
    }
    return render(request, 'cart/detail.html', context)


@require_POST
def cart_add(request):
    """ Adding product to Cart """
    product_id = request.POST.get('product_id')
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponse(_('Product does not exist!'), status=404)
    else:
        cart = Cart(request)
        cart.add(
            product_id=product_id,
            quantity=int(request.POST.get('quantity')),
        )

        if request.LANGUAGE_CODE == 'en':
            product_name = product.name
        else:
            for product_translation in product.translations.all():
                if product_translation.language == request.LANGUAGE_CODE:
                    product_name = product_translation.name
                    break

        currency_code = request.session.get('currency_code')

        product_price = get_value_in_currency(product.price, currency_code)
        product_price = str(product_price).split('.')

        cart_total_price = cart.get_total_price()
        cart_total_price = get_value_in_currency(
            cart_total_price, currency_code)
        cart_total_price = str(cart_total_price).split('.')

        data = {
            'cart_len': len(cart),
            'cart_total_price': cart_total_price,
            'product_name': product_name,
            'product_main_image_url': product.main_image.url,
            'product_price': product_price,
            'product_quantity': cart.cart[product_id]['quantity'],
        }
        return JsonResponse(data)


@require_POST
def cart_update(request):
    """ Update quantity of products in Cart """
    item_ids = request.POST.get('item_ids').split()
    item_quantities = request.POST.get('item_quantities').split()
    products = Product.objects.filter(id__in=item_ids)

    cart = Cart(request)
    currency_code = request.session.get('currency_code')
    item_total_prices = []

    for item in zip(item_ids, item_quantities):
        cart.update(item[0], int(item[1]))

        product = products.get(id=item[0])
        total_price = product.price * cart.cart[item[0]]['quantity']
        total_price = get_value_in_currency(total_price, currency_code)
        total_price = str(total_price).split('.')
        item_total_prices.append(total_price)

    cart_total_price = cart.get_total_price()
    cart_total_price = get_value_in_currency(cart_total_price, currency_code)
    cart_total_price = str(cart_total_price).split('.')

    cart_total_cost = cart.get_total_cost()
    cart_total_cost = get_value_in_currency(cart_total_cost, currency_code)
    cart_total_cost = str(cart_total_cost).split('.')

    data = {
        'cart_len': len(cart),
        'cart_total_price': cart_total_price,
        'cart_total_cost': cart_total_cost,
        'item_total_prices': item_total_prices,
    }
    return JsonResponse(data)


@require_POST
def cart_remove(request):
    """ Removing product from Cart """
    product_id = request.POST.get('product_id')

    cart = Cart(request)
    cart.remove(product_id)

    currency_code = request.session.get('currency_code')

    cart_total_price = cart.get_total_price()
    cart_total_price = get_value_in_currency(cart_total_price, currency_code)
    cart_total_price = str(cart_total_price).split('.')

    cart_total_cost = cart.get_total_cost()
    cart_total_cost = get_value_in_currency(cart_total_cost, currency_code)
    cart_total_cost = str(cart_total_cost).split('.')

    data = {
        'cart_len': len(cart),
        'cart_total_price': cart_total_price,
        'cart_total_cost': cart_total_cost,
    }
    return JsonResponse(data)
