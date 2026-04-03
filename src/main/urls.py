from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),

    path('about/', views.about, name='about'),
    path('delivery/', views.delivery, name='delivery'),

    path('set/language/<str:language_code>/',
        views.set_language,
        name='set_language'),
    path('set/currency/<str:currency_code>/',
        views.set_currency,
        name='set_currency'),
    path('set/city/<str:city_code>/', views.set_city, name='set_city'),
]
