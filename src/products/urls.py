from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('search/', views.search, name='search'),

    path('shop/', views.shop, name='shop'),
    path('manufacturer/<str:m_slug>/', views.manufacturer, name='manufacturer'),

    path('product/<int:p_id>/', views.product_detail, name='product_detail'),

    path('comics/', views.comics, name='comics'),
    path('comics/<str:p_slug>/',
        views.comic_book_detail,
        name='comic_book_detail'),

    path('toys/', views.toys, name='toys'),
    path('toys/<str:p_slug>/', views.toy_detail, name='toy_detail'),

    path('clothes/', views.clothes, name='clothes'),
    path('clothes/<str:p_slug>/', views.clothes_detail, name='clothes_detail'),

    path('accessories/', views.accessories, name='accessories'),
    path('accessories/<str:p_slug>/',
        views.accessory_detail,
        name='accessory_detail'),

    path('home-decor/', views.home_decor, name='home_decor'),
    path('home-decor/<str:p_slug>/',
        views.home_decor_detail,
        name='home_decor_detail'),

    path('review/add/<int:p_id>/', views.review_add, name='review_add'),
    path('review/like/', views.review_like, name='review_like'),
    path('review/dislike/', views.review_dislike, name='review_dislike'),

    path('set/sort/<str:products_sort>/', views.set_sort, name='set_sort'),
    path('set/view/<str:products_view>/', views.set_view, name='set_view'),
]
