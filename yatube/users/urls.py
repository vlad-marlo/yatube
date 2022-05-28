from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    path(
        'logout',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    path(
        'login',
        views.SignUp.as_view(),
        name='signup',
    ),
]
