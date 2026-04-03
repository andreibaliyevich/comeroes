from django.urls import path
from . import views


app_name = 'support'

urlpatterns = [
    path('', views.SupportView.as_view(), name='support'),
    path('tickets/', views.tickets, name='tickets'),
    path('tickets/<int:t_id>/detail/',
        views.ticket_detail,
        name='ticket_detail'),
]
