from django.urls import path
from .views import (
    CustomLoginView, 
    RegistrationView, 
    dashboard, 
    password_reset1, 
    password_reset, 
    password_reset_confirm
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('reset-password/', password_reset1, name='password_reset1'),
    path('reset-password/code/', password_reset, name='password_reset'),
    path('reset-password/confirm/', password_reset_confirm, name='password_reset_confirm'),
]