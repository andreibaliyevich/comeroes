from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),

    path('signup/', views.signup, name='signup'),
    path('signup/activate/<str:sign>/',
        views.signup_activate,
        name='signup_activate'),

    path('password/reset/',
        views.OSPasswordResetView.as_view(),
        name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/',
        views.OSPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path('password/change/',
        views.OSPasswordChangeView.as_view(),
        name='password_change'),

    path('profile/', views.profile, name='profile'),
    path('profile/delete/', views.profile_delete, name='profile_delete'),

    path('addresses/', views.addresses, name='addresses'),
    path('address/<int:address_id>/change/',
        views.address_change,
        name='address_change'),
    path('address/<int:address_id>/delete/',
        views.address_delete,
        name='address_delete'),
]
