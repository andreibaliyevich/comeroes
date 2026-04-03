from operator import attrgetter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from main.services import get_price_range_from_currency
from .forms import (
    SortingForm,
    ManufacturerFilter,
    ComicBookFilter,
    ToyFilter,
    ClothesFilter,
    AccessoryFilter,
    HomeDecorFilter,
    ReviewForm,
)
from .models import (
    Manufacturer,
    Product,
    ComicBookProduct,
    ToyProduct,
    ClothesProduct,
    AccessoryProduct,
    HomeDecorProduct,
    Warehouse,
    Review,
)
from .services import sort_products_by_name, get_stats_of_reviews


def search(request):
    """ Search for products """
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    sorting_form = SortingForm()

    if category == 'comics':
        products = ComicBookProduct.objects.search(query)
    elif category == 'toys':
        products = ToyProduct.objects.search(query)
    elif category == 'clothes':
        products = ClothesProduct.objects.search(query)
    elif category == 'accessories':
        products = AccessoryProduct.objects.search(query)
    elif category == 'home_decor':
        products = HomeDecorProduct.objects.search(query)
    else:
        products = Product.objects.search(query)

    if 'products_sort' in request.session:
        type_sort = request.session.get('products_sort')
        sorting_form.fields['type_sort'].initial = type_sort

        if type_sort == 'popularity':
            products = products.order_by('-rating', 'id')
        elif type_sort == 'new_old':
            products = products.order_by('-created_at', 'id')
        elif type_sort == 'old_new':
            products = products.order_by('created_at', 'id')
        elif type_sort == 'low_high_price':
            products = products.order_by('price', 'id')
        elif type_sort == 'high_low_price':
            products = products.order_by('-price', 'id')
        elif type_sort == 'az_order':
            products = sort_products_by_name(products)
        elif type_sort == 'za_order':
            products = sort_products_by_name(products, reverse=True)
    else:
        products = products.order_by('-rating', 'id')

    paginator = Paginator(products, 20)
    page_number = request.GET.get('page', 1)
    objects_page = paginator.get_page(page_number)

    context = {
        'sorting_form': sorting_form,
        'objects_page': objects_page,
    }

    if 'products_view' in request.session:
        if request.session.get('products_view') == 'grid':
            return render(request, 'products/grid/search.html', context)
        elif request.session.get('products_view') == 'list':
            return render(request, 'products/list/search.html', context)
    return render(request, 'products/grid/search.html', context)


def shop(request):
    """ Shop """
    comicbook_categories = []
    toy_categories = []
    clothes_categories = []
    accessory_categories = []
    homedecor_categories = []

    for category in ComicBookProduct.CATEGORY_CHOICES[1:]:
        product_count = ComicBookProduct.objects.filter(
            category=category[0]).count()
        comicbook_categories.append((category[0], category[1], product_count))

    for category in ToyProduct.CATEGORY_CHOICES[1:]:
        product_count = ToyProduct.objects.filter(
            category=category[0]).count()
        toy_categories.append((category[0], category[1], product_count))

    for category in ClothesProduct.CATEGORY_CHOICES[1:]:
        product_count = ClothesProduct.objects.filter(
            category=category[0]).count()
        clothes_categories.append((category[0], category[1], product_count))

    for category in AccessoryProduct.CATEGORY_CHOICES[1:]:
        product_count = AccessoryProduct.objects.filter(
            category=category[0]).count()
        accessory_categories.append((category[0], category[1], product_count))

    for category in HomeDecorProduct.CATEGORY_CHOICES[1:]:
        product_count = HomeDecorProduct.objects.filter(
            category=category[0]).count()
        homedecor_categories.append((category[0], category[1], product_count))

    comics_count = ComicBookProduct.objects.count()
    toys_count = ToyProduct.objects.count()
    clothes_count = ClothesProduct.objects.count()
    accessories_count = AccessoryProduct.objects.count()
    home_decor_count = HomeDecorProduct.objects.count()

    manufacturers = Manufacturer.objects.all()

    context = {
        'comicbook_categories': comicbook_categories,
        'comics_count': comics_count,
        'toy_categories': toy_categories,
        'toys_count': toys_count,
        'clothes_categories': clothes_categories,
        'clothes_count': clothes_count,
        'accessory_categories': accessory_categories,
        'accessories_count': accessories_count,
        'homedecor_categories': homedecor_categories,
        'home_decor_count': home_decor_count,
        'manufacturers': manufacturers,
    }
    return render(request, 'products/shop.html', context)


def manufacturer(request, m_slug):
    """ Products by manufacturer """
    manufacturer = get_object_or_404(Manufacturer, slug=m_slug)
    sorting_form = SortingForm()
    manufacturer_filter = ManufacturerFilter(request.GET or None)

    product_ids = []

    if request.GET:
        if manufacturer_filter.is_valid():
            filter_cd = manufacturer_filter.cleaned_data

            if filter_cd['categories']:
                if '1' in filter_cd['categories']:
                    product_ids += list(ComicBookProduct.objects.filter(
                        manufacturer=manufacturer,
                    ).values_list('id', flat=True))
                if '2' in filter_cd['categories']:
                    product_ids += list(ToyProduct.objects.filter(
                        manufacturer=manufacturer,
                    ).values_list('id', flat=True))
                if '3' in filter_cd['categories']:
                    product_ids += list(ClothesProduct.objects.filter(
                        manufacturer=manufacturer,
                    ).values_list('id', flat=True))
                if '4' in filter_cd['categories']:
                    product_ids += list(AccessoryProduct.objects.filter(
                        manufacturer=manufacturer,
                    ).values_list('id', flat=True))
                if '5' in filter_cd['categories']:
                    product_ids += list(HomeDecorProduct.objects.filter(
                        manufacturer=manufacturer,
                    ).values_list('id', flat=True))
            else:
                product_ids += list(Product.objects.filter(
                    manufacturer=manufacturer,
                ).values_list('id', flat=True))

            products = Product.objects.filter(id__in=product_ids)

            if filter_cd['min_price'] and filter_cd['max_price']:
                min_price, max_price = get_price_range_from_currency(
                    f_min_price=int(filter_cd['min_price']),
                    f_max_price=int(filter_cd['max_price']),
                    currency_code=request.session.get('currency_code'),
                )
                products = products.filter(
                    price__range=(min_price, max_price),
                )
    else:
        products = Product.objects.filter(manufacturer=manufacturer)

    if 'products_sort' in request.session:
        type_sort = request.session.get('products_sort')
        sorting_form.fields['type_sort'].initial = type_sort

        if type_sort == 'popularity':
            products = products.order_by('-rating', 'id')
        elif type_sort == 'new_old':
            products = products.order_by('-created_at', 'id')
        elif type_sort == 'old_new':
            products = products.order_by('created_at', 'id')
        elif type_sort == 'low_high_price':
            products = products.order_by('price', 'id')
        elif type_sort == 'high_low_price':
            products = products.order_by('-price', 'id')
        elif type_sort == 'az_order':
            products = sort_products_by_name(products)
        elif type_sort == 'za_order':
            products = sort_products_by_name(products, reverse=True)
    else:
        products = products.order_by('-rating', 'id')

    paginator = Paginator(products, 15)
    page_number = request.GET.get('page', 1)
    objects_page = paginator.get_page(page_number)

    context = {
        'manufacturer': manufacturer,
        'sorting_form': sorting_form,
        'manufacturer_filter': manufacturer_filter,
        'objects_page': objects_page,
    }

    if 'products_view' in request.session:
        if request.session.get('products_view') == 'grid':
            return render(request, 'products/grid/manufacturer.html', context)
        elif request.session.get('products_view') == 'list':
            return render(request, 'products/list/manufacturer.html', context)
    return render(request, 'products/grid/manufacturer.html', context)


def product_detail(request, p_id):
    """ Product Detail """
    try:
        product = ComicBookProduct.objects.get(id=p_id)
    except ComicBookProduct.DoesNotExist:
        try:
            product = ToyProduct.objects.get(id=p_id)
        except ToyProduct.DoesNotExist:
            try:
                product = ClothesProduct.objects.get(id=p_id)
            except ClothesProduct.DoesNotExist:
                try:
                    product = AccessoryProduct.objects.get(id=p_id)
                except AccessoryProduct.DoesNotExist:
                    try:
                        product = HomeDecorProduct.objects.get(id=p_id)
                    except HomeDecorProduct.DoesNotExist:
                        raise Http404
    return redirect(product)


def comics(request):
    """ Comics """
    sorting_form = SortingForm()
    product_filter = ComicBookFilter(request.GET or None)
    products = ComicBookProduct.objects.all()

    if request.GET:
        if product_filter.is_valid():
            filter_cd = product_filter.cleaned_data

            if filter_cd['min_price'] and filter_cd['max_price']:
                min_price, max_price = get_price_range_from_currency(
                    f_min_price=int(filter_cd['min_price']),
                    f_max_price=int(filter_cd['max_price']),
                    currency_code=request.session.get('currency_code'),
                )
                products = products.filter(
                    price__range=(min_price, max_price),
                )

            if filter_cd['categories']:
                products = products.filter(
                    category__in=filter_cd['categories'],
                )

            if filter_cd['languages']:
                products = products.filter(
                    language__in=filter_cd['languages'],
                )

    if 'products_sort' in request.session:
        type_sort = request.session.get('products_sort')
        sorting_form.fields['type_sort'].initial = type_sort

        if type_sort == 'popularity':
            products = products.order_by('-rating', 'id')
        elif type_sort == 'new_old':
            products = products.order_by('-published', 'id')
        elif type_sort == 'old_new':
            products = products.order_by('published', 'id')
        elif type_sort == 'low_high_price':
            products = products.order_by('price', 'id')
        elif type_sort == 'high_low_price':
            products = products.order_by('-price', 'id')
        elif type_sort == 'az_order':
            products = sort_products_by_name(products)
        elif type_sort == 'za_order':
            products = sort_products_by_name(products, reverse=True)
    else:
        products = products.order_by('-rating', 'id')

    paginator = Paginator(products, 15)
    page_number = request.GET.get('page', 1)
    objects_page = paginator.get_page(page_number)

    context = {
        'sorting_form': sorting_form,
        'product_filter': product_filter,
        'objects_page': objects_page,
    }

    if 'products_view' in request.session:
        if request.session.get('products_view') == 'grid':
            return render(request, 'products/grid/comics.html', context)
        elif request.session.get('products_view') == 'list':
            return render(request, 'products/list/comics.html', context)
    return render(request, 'products/grid/comics.html', context)


def comic_book_detail(request, p_slug):
    """ Comic Book Detail """
    product = get_object_or_404(ComicBookProduct, slug=p_slug)
    product_images = product.productimage_set.all()

    warehouses = Warehouse.objects.filter(
        product=product,
        store__city=request.session['city_code'],
    )
    if warehouses:
        product_available = True
    else:
        product_available = False

    reviews = product.review_set.all()
    stats_of_reviews = get_stats_of_reviews(reviews)
    review_form = ReviewForm()

    similar_products = ComicBookProduct.objects.all().order_by('-rating', 'id')
    similar_products = similar_products.exclude(id=product.id)
    similar_products = similar_products[:5]

    toys = ToyProduct.objects.all().order_by('-rating', 'id')[:2]
    clothes = ClothesProduct.objects.all().order_by('-rating', 'id')[:2]
    accessories = AccessoryProduct.objects.all().order_by('-rating', 'id')[:2]
    home_decor = HomeDecorProduct.objects.all().order_by('-rating', 'id')[:2]
    other_products = []
    for toy_product in toys:
        other_products.append(toy_product)
    for clothes_product in clothes:
        other_products.append(clothes_product)
    for accessory_product in accessories:
        other_products.append(accessory_product)
    for home_decor_product in home_decor:
        other_products.append(home_decor_product)

    context = {
        'product': product,
        'product_images': product_images,
        'product_available': product_available,
        'reviews': reviews,
        'stats_of_reviews': stats_of_reviews,
        'review_form': review_form,
        'similar_products': similar_products,
        'other_products': other_products,
    }
    return render(request, 'products/detail/comic_book.html', context)


def toys(request):
    """ Toys """
    sorting_form = SortingForm()
    product_filter = ToyFilter(request.GET or None)
    products = ToyProduct.objects.all()

    if request.GET:
        if product_filter.is_valid():
            filter_cd = product_filter.cleaned_data

            if filter_cd['min_price'] and filter_cd['max_price']:
                min_price, max_price = get_price_range_from_currency(
                    f_min_price=int(filter_cd['min_price']),
                    f_max_price=int(filter_cd['max_price']),
                    currency_code=request.session.get('currency_code'),
                )
                products = products.filter(
                    price__range=(min_price, max_price),
                )

            if filter_cd['categories']:
                products = products.filter(
                    category__in=filter_cd['categories'],
                )

            if filter_cd['countries']:
                products = products.filter(
                    country__in=filter_cd['countries'],
                )

            if filter_cd['materials']:
                products = products.filter(
                    material__in=filter_cd['materials'],
                )

    if 'products_sort' in request.session:
        type_sort = request.session.get('products_sort')
        sorting_form.fields['type_sort'].initial = type_sort

        if type_sort == 'popularity':
            products = products.order_by('-rating', 'id')
        elif type_sort == 'new_old':
            products = products.order_by('-created_at', 'id')
        elif type_sort == 'old_new':
            products = products.order_by('created_at', 'id')
        elif type_sort == 'low_high_price':
            products = products.order_by('price', 'id')
        elif type_sort == 'high_low_price':
            products = products.order_by('-price', 'id')
        elif type_sort == 'az_order':
            products = sort_products_by_name(products)
        elif type_sort == 'za_order':
            products = sort_products_by_name(products, reverse=True)
    else:
        products = products.order_by('-rating', 'id')

    paginator = Paginator(products, 15)
    page_number = request.GET.get('page', 1)
    objects_page = paginator.get_page(page_number)

    context = {
        'sorting_form': sorting_form,
        'product_filter': product_filter,
        'objects_page': objects_page,
    }

    if 'products_view' in request.session:
        if request.session.get('products_view') == 'grid':
            return render(request, 'products/grid/toys.html', context)
        elif request.session.get('products_view') == 'list':
            return render(request, 'products/list/toys.html', context)
    return render(request, 'products/grid/toys.html', context)


def toy_detail(request, p_slug):
    """ Toy Detail """
    product = get_object_or_404(ToyProduct, slug=p_slug)
    product_images = product.productimage_set.all()

    warehouses = Warehouse.objects.filter(
        product=product,
        store__city=request.session['city_code'],
    )
    if warehouses:
        product_available = True
    else:
        product_available = False

    reviews = product.review_set.all()
    stats_of_reviews = get_stats_of_reviews(reviews)
    review_form = ReviewForm()

    similar_products = ToyProduct.objects.all().order_by('-rating', 'id')
    similar_products = similar_products.exclude(id=product.id)
    similar_products = similar_products[:5]

    comics = ComicBookProduct.objects.all().order_by('-rating', 'id')[:2]
    clothes = ClothesProduct.objects.all().order_by('-rating', 'id')[:2]
    accessories = AccessoryProduct.objects.all().order_by('-rating', 'id')[:2]
    home_decor = HomeDecorProduct.objects.all().order_by('-rating', 'id')[:2]
    other_products = []
    for comic_product in comics:
        other_products.append(comic_product)
    for clothes_product in clothes:
        other_products.append(clothes_product)
    for accessory_product in accessories:
        other_products.append(accessory_product)
    for home_decor_product in home_decor:
        other_products.append(home_decor_product)

    context = {
        'product': product,
        'product_images': product_images,
        'product_available': product_available,
        'reviews': reviews,
        'stats_of_reviews': stats_of_reviews,
        'review_form': review_form,
        'similar_products': similar_products,
        'other_products': other_products,
    }
    return render(request, 'products/detail/toy.html', context)


def clothes(request):
    """ Clothes """
    sorting_form = SortingForm()
    product_filter = ClothesFilter(request.GET or None)
    products = ClothesProduct.objects.all()

    if request.GET:
        if product_filter.is_valid():
            filter_cd = product_filter.cleaned_data

            if filter_cd['min_price'] and filter_cd['max_price']:
                min_price, max_price = get_price_range_from_currency(
                    f_min_price=int(filter_cd['min_price']),
                    f_max_price=int(filter_cd['max_price']),
                    currency_code=request.session.get('currency_code'),
                )
                products = products.filter(
                    price__range=(min_price, max_price),
                )

            if filter_cd['categories']:
                products = products.filter(
                    category__in=filter_cd['categories'],
                )

            if filter_cd['sizes']:
                products = products.filter(
                    size__in=filter_cd['sizes'],
                )

            if filter_cd['colors']:
                products = products.filter(
                    color__in=filter_cd['colors'],
                )

    if 'products_sort' in request.session:
        type_sort = request.session.get('products_sort')
        sorting_form.fields['type_sort'].initial = type_sort

        if type_sort == 'popularity':
            products = products.order_by('-rating', 'id')
        elif type_sort == 'new_old':
            products = products.order_by('-created_at', 'id')
        elif type_sort == 'old_new':
            products = products.order_by('created_at', 'id')
        elif type_sort == 'low_high_price':
            products = products.order_by('price', 'id')
        elif type_sort == 'high_low_price':
            products = products.order_by('-price', 'id')
        elif type_sort == 'az_order':
            products = sort_products_by_name(products)
        elif type_sort == 'za_order':
            products = sort_products_by_name(products, reverse=True)
    else:
        products = products.order_by('-rating', 'id')

    paginator = Paginator(products, 15)
    page_number = request.GET.get('page', 1)
    objects_page = paginator.get_page(page_number)

    context = {
        'sorting_form': sorting_form,
        'product_filter': product_filter,
        'objects_page': objects_page,
    }

    if 'products_view' in request.session:
        if request.session.get('products_view') == 'grid':
            return render(request, 'products/grid/clothes.html', context)
        elif request.session.get('products_view') == 'list':
            return render(request, 'products/list/clothes.html', context)
    return render(request, 'products/grid/clothes.html', context)


def clothes_detail(request, p_slug):
    """ Clothes Detail """
    product = get_object_or_404(ClothesProduct, slug=p_slug)
    product_images = product.productimage_set.all()

    warehouses = Warehouse.objects.filter(
        product=product,
        store__city=request.session['city_code'],
    )
    if warehouses:
        product_available = True
    else:
        product_available = False

    reviews = product.review_set.all()
    stats_of_reviews = get_stats_of_reviews(reviews)
    review_form = ReviewForm()

    similar_products = ClothesProduct.objects.all().order_by('-rating', 'id')
    similar_products = similar_products.exclude(id=product.id)
    similar_products = similar_products[:5]

    comics = ComicBookProduct.objects.all().order_by('-rating', 'id')[:2]
    toys = ToyProduct.objects.all().order_by('-rating', 'id')[:2]
    accessories = AccessoryProduct.objects.all().order_by('-rating', 'id')[:2]
    home_decor = HomeDecorProduct.objects.all().order_by('-rating', 'id')[:2]
    other_products = []
    for comic_product in comics:
        other_products.append(comic_product)
    for toy_product in toys:
        other_products.append(toy_product)
    for accessory_product in accessories:
        other_products.append(accessory_product)
    for home_decor_product in home_decor:
        other_products.append(home_decor_product)

    context = {
        'product': product,
        'product_images': product_images,
        'product_available': product_available,
        'reviews': reviews,
        'stats_of_reviews': stats_of_reviews,
        'review_form': review_form,
        'similar_products': similar_products,
        'other_products': other_products,
    }
    return render(request, 'products/detail/clothes.html', context)


def accessories(request):
    """ Accessories """
    sorting_form = SortingForm()
    product_filter = AccessoryFilter(request.GET or None)
    products = AccessoryProduct.objects.all()

    if request.GET:
        if product_filter.is_valid():
            filter_cd = product_filter.cleaned_data

            if filter_cd['min_price'] and filter_cd['max_price']:
                min_price, max_price = get_price_range_from_currency(
                    f_min_price=int(filter_cd['min_price']),
                    f_max_price=int(filter_cd['max_price']),
                    currency_code=request.session.get('currency_code'),
                )
                products = products.filter(
                    price__range=(min_price, max_price),
                )

            if filter_cd['categories']:
                products = products.filter(
                    category__in=filter_cd['categories'],
                )

    if 'products_sort' in request.session:
        type_sort = request.session.get('products_sort')
        sorting_form.fields['type_sort'].initial = type_sort

        if type_sort == 'popularity':
            products = products.order_by('-rating', 'id')
        elif type_sort == 'new_old':
            products = products.order_by('-created_at', 'id')
        elif type_sort == 'old_new':
            products = products.order_by('created_at', 'id')
        elif type_sort == 'low_high_price':
            products = products.order_by('price', 'id')
        elif type_sort == 'high_low_price':
            products = products.order_by('-price', 'id')
        elif type_sort == 'az_order':
            products = sort_products_by_name(products)
        elif type_sort == 'za_order':
            products = sort_products_by_name(products, reverse=True)
    else:
        products = products.order_by('-rating', 'id')

    paginator = Paginator(products, 15)
    page_number = request.GET.get('page', 1)
    objects_page = paginator.get_page(page_number)

    context = {
        'sorting_form': sorting_form,
        'product_filter': product_filter,
        'objects_page': objects_page,
    }

    if 'products_view' in request.session:
        if request.session.get('products_view') == 'grid':
            return render(request, 'products/grid/accessories.html', context)
        elif request.session.get('products_view') == 'list':
            return render(request, 'products/list/accessories.html', context)
    return render(request, 'products/grid/accessories.html', context)


def accessory_detail(request, p_slug):
    """ Accessory Detail """
    product = get_object_or_404(AccessoryProduct, slug=p_slug)
    product_images = product.productimage_set.all()

    warehouses = Warehouse.objects.filter(
        product=product,
        store__city=request.session['city_code'],
    )
    if warehouses:
        product_available = True
    else:
        product_available = False

    reviews = product.review_set.all()
    stats_of_reviews = get_stats_of_reviews(reviews)
    review_form = ReviewForm()

    similar_products = AccessoryProduct.objects.all().order_by('-rating', 'id')
    similar_products = similar_products.exclude(id=product.id)
    similar_products = similar_products[:5]

    comics = ComicBookProduct.objects.all().order_by('-rating', 'id')[:2]
    toys = ToyProduct.objects.all().order_by('-rating', 'id')[:2]
    clothes = ClothesProduct.objects.all().order_by('-rating', 'id')[:2]
    home_decor = HomeDecorProduct.objects.all().order_by('-rating', 'id')[:2]
    other_products = []
    for comic_product in comics:
        other_products.append(comic_product)
    for toy_product in toys:
        other_products.append(toy_product)
    for clothes_product in clothes:
        other_products.append(clothes_product)
    for home_decor_product in home_decor:
        other_products.append(home_decor_product)

    context = {
        'product': product,
        'product_images': product_images,
        'product_available': product_available,
        'reviews': reviews,
        'stats_of_reviews': stats_of_reviews,
        'review_form': review_form,
        'similar_products': similar_products,
        'other_products': other_products,
    }
    return render(request, 'products/detail/accessory.html', context)


def home_decor(request):
    """ Home Decor """
    sorting_form = SortingForm()
    product_filter = HomeDecorFilter(request.GET or None)
    products = HomeDecorProduct.objects.all()

    if request.GET:
        if product_filter.is_valid():
            filter_cd = product_filter.cleaned_data

            if filter_cd['min_price'] and filter_cd['max_price']:
                min_price, max_price = get_price_range_from_currency(
                    f_min_price=int(filter_cd['min_price']),
                    f_max_price=int(filter_cd['max_price']),
                    currency_code=request.session.get('currency_code'),
                )
                products = products.filter(
                    price__range=(min_price, max_price),
                )

            if filter_cd['categories']:
                products = products.filter(
                    category__in=filter_cd['categories'],
                )

    if 'products_sort' in request.session:
        type_sort = request.session.get('products_sort')
        sorting_form.fields['type_sort'].initial = type_sort

        if type_sort == 'popularity':
            products = products.order_by('-rating', 'id')
        elif type_sort == 'new_old':
            products = products.order_by('-created_at', 'id')
        elif type_sort == 'old_new':
            products = products.order_by('created_at', 'id')
        elif type_sort == 'low_high_price':
            products = products.order_by('price', 'id')
        elif type_sort == 'high_low_price':
            products = products.order_by('-price', 'id')
        elif type_sort == 'az_order':
            products = sort_products_by_name(products)
        elif type_sort == 'za_order':
            products = sort_products_by_name(products, reverse=True)
    else:
        products = products.order_by('-rating', 'id')

    paginator = Paginator(products, 15)
    page_number = request.GET.get('page', 1)
    objects_page = paginator.get_page(page_number)

    context = {
        'sorting_form': sorting_form,
        'product_filter': product_filter,
        'objects_page': objects_page,
    }

    if 'products_view' in request.session:
        if request.session.get('products_view') == 'grid':
            return render(request, 'products/grid/home_decor.html', context)
        elif request.session.get('products_view') == 'list':
            return render(request, 'products/list/home_decor.html', context)
    return render(request, 'products/grid/home_decor.html', context)


def home_decor_detail(request, p_slug):
    """ Home Decor Detail """
    product = get_object_or_404(HomeDecorProduct, slug=p_slug)
    product_images = product.productimage_set.all()

    warehouses = Warehouse.objects.filter(
        product=product,
        store__city=request.session['city_code'],
    )
    if warehouses:
        product_available = True
    else:
        product_available = False

    reviews = product.review_set.all()
    stats_of_reviews = get_stats_of_reviews(reviews)
    review_form = ReviewForm()

    similar_products = HomeDecorProduct.objects.all().order_by('-rating', 'id')
    similar_products = similar_products.exclude(id=product.id)
    similar_products = similar_products[:5]

    comics = ComicBookProduct.objects.all().order_by('-rating', 'id')[:2]
    toys = ToyProduct.objects.all().order_by('-rating', 'id')[:2]
    clothes = ClothesProduct.objects.all().order_by('-rating', 'id')[:2]
    accessories = AccessoryProduct.objects.all().order_by('-rating', 'id')[:2]
    other_products = []
    for comic_product in comics:
        other_products.append(comic_product)
    for toy_product in toys:
        other_products.append(toy_product)
    for clothes_product in clothes:
        other_products.append(clothes_product)
    for accessory_product in accessories:
        other_products.append(accessory_product)

    context = {
        'product': product,
        'product_images': product_images,
        'product_available': product_available,
        'reviews': reviews,
        'stats_of_reviews': stats_of_reviews,
        'review_form': review_form,
        'similar_products': similar_products,
        'other_products': other_products,
    }
    return render(request, 'products/detail/home_decor.html', context)


@login_required
@require_POST
def review_add(request, p_id):
    """ Add a review """
    try:
        product = Product.objects.get(id=p_id)
    except Product.DoesNotExist:
        return HttpResponse(_('Product does not exist!'), status=404)
    else:
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.user = request.user

            try:
                new_review.save()
            except IntegrityError:
                message = _('You have already left a review for this product.')
                messages.error(request, message)
            else:
                message = _('Thanks for your review.')
                messages.success(request, message)

        next_page = request.META.get('HTTP_REFERER', '/')
        return redirect(next_page)


@login_required
@require_POST
def review_like(request):
    """ Like a review """
    try:
        review = Review.objects.get(id=request.POST.get('review_id'))
    except Review.DoesNotExist:
        return HttpResponse(_('Review does not exist!'), status=404)
    else:
        if request.user in review.likes.all():
            review.likes.remove(request.user)
        elif request.user in review.dislikes.all():
            review.dislikes.remove(request.user)
            review.likes.add(request.user)
        else:
            review.likes.add(request.user)

        data = {
            'likes_count': review.likes.count(),
            'dislikes_count': review.dislikes.count(),
        }
        return JsonResponse(data)


@login_required
@require_POST
def review_dislike(request):
    """ Dislike a review """
    try:
        review = Review.objects.get(id=request.POST.get('review_id'))
    except Review.DoesNotExist:
        return HttpResponse(_('Review does not exist!'), status=404)
    else:
        if request.user in review.dislikes.all():
            review.dislikes.remove(request.user)
        elif request.user in review.likes.all():
            review.likes.remove(request.user)
            review.dislikes.add(request.user)
        else:
            review.dislikes.add(request.user)

        data = {
            'likes_count': review.likes.count(),
            'dislikes_count': review.dislikes.count(),
        }
        return JsonResponse(data)


def set_sort(request, products_sort):
    """ Set sort """
    request.session['products_sort'] = products_sort
    next_page = request.META.get('HTTP_REFERER', '/')
    return redirect(next_page)


def set_view(request, products_view):
    """ Set view """
    request.session['products_view'] = products_view
    next_page = request.META.get('HTTP_REFERER', '/')
    return redirect(next_page)
