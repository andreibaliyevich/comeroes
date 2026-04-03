from django.urls import path
from . import views


app_name = 'contacts'

urlpatterns = [
    path('contacts/', views.contacts, name='contacts'),
    path('store/<int:s_id>/detail/', views.store_detail, name='store_detail'),
]
