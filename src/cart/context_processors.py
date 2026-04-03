from .cart import Cart


def cart_context(request):
    context = {
        'cart': Cart(request),
    }
    return context
