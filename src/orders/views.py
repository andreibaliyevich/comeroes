from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from accounts.models import Address
from wishlist.models import Wish
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem


@login_required
def orders_list(request):
    """ Orders list """
    objects = request.user.order_set.all()

    paginator = Paginator(objects, 8)
    page_number = request.GET.get('page', 1)
    objects_page = paginator.get_page(page_number)

    context = {
        'objects_page': objects_page,
    }
    return render(request, 'orders/list.html', context)


@login_required
def order_detail(request, o_id):
    """ Order Detail """
    order = get_object_or_404(Order, id=o_id)

    if order.user.id == request.user.id:
        context = {
            'order': order,
        }
        return render(request, 'orders/detail.html', context)
    else:
        raise Http404


def order_create(request):
    """ Order create """
    if request.method == 'POST':
        order_create_form = OrderCreateForm(request, request.POST)

        if order_create_form.is_valid():
            cart = Cart(request)
            order = order_create_form.save(commit=False)

            if request.user.is_authenticated:
                order.user = request.user

            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount

            order.total_cost = cart.get_total_cost()
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['product'].price,
                    quantity=item['quantity'],
                    total_price=item['total_price'],
                )

                try:
                    wish = Wish.objects.get(
                        user=request.user,
                        product=item['product'],
                    )
                except Wish.DoesNotExist:
                    pass
                else:
                    wish.delete()

            cart.clear()

            context = {
                'order_id': order.id,
                'order_absolute_url': order.get_absolute_url(),
            }
            return render(request, 'orders/complete.html', context)

    else:
        if request.user.is_authenticated:
            order_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone': request.user.phone,
            }

            try:
                address = Address.objects.get(
                    user=request.user,
                    is_primary=True,
                )
            except Address.DoesNotExist:
                pass
            else:
                order_data['address'] = (
                    f'{ address.locality }, { address.street_house }'
                )
                if address.porch:
                    order_data['address'] += f', { address.porch }'
                if address.level:
                    order_data['address'] += f', { address.level }'
                if address.apt_office:
                    order_data['address'] += f', { address.apt_office }'

            order_create_form = OrderCreateForm(request, initial=order_data)
        else:
            order_create_form = OrderCreateForm(request)

    context = {
        'order_create_form': order_create_form,
    }
    return render(request, 'orders/create.html', context)
