from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Wish


@login_required
def wishlist(request):
    """ Wishlist """
    wishes_list = request.user.wish_set.all()

    context = {
        'wishes_list': wishes_list,
    }
    return render(request, 'wishlist/list.html', context)


@login_required
@require_POST
def wish_add(request):
    """ Adding product to Wishlist """
    product_id = int(request.POST.get('product_id'))
    try:
        product = Product.objects.get(id=product_id)
        Wish.objects.create(user=request.user, product=product)
    except Product.DoesNotExist:
        return HttpResponse(_('Product does not exist!'), status=404)
    except IntegrityError:
        return JsonResponse({
            'message': _('This product has already been added to your wishlist.')
        })
    else:
        return JsonResponse({
            'message': _('This product has been added to your wishlist.')
        })


@login_required
@require_POST
def wish_remove(request):
    """ Removing product from Wishlist """
    wish_id = int(request.POST.get('wish_id'))
    try:
        wish = Wish.objects.get(id=wish_id)
    except Wish.DoesNotExist:
        return HttpResponse(_('Wish does not exist!'), status=404)
    else:
        if wish.user.id == request.user.id:
            wish.delete()
            return JsonResponse({
                'wishes_count': request.user.wish_set.count()
            })
        else:
            return HttpResponse(_('Wish does not exist!'), status=404)
