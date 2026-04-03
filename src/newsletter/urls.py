from django.urls import path
from . import views


app_name = 'newsletter'

urlpatterns = [
    path('subscriber/add/', views.subscriber_add, name='subscriber_add'),
    path('subscriber/confirm/<str:sign>/',
        views.subscriber_confirm,
        name='subscriber_confirm'),
    path('subscriber/delete/<str:sign>/',
        views.subscriber_delete,
        name='subscriber_delete'),
]
