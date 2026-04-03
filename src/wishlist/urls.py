from django.urls import path
from . import views


app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist, name='wishlist'),
    path('add/', views.wish_add, name='wish_add'),
    path('remove/', views.wish_remove, name='wish_remove'),
]
