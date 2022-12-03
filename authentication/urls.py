from django.contrib import admin
from django.urls import path
from . import views as auth_view

urlpatterns = [
    path('login', auth_view.login_page, name='login'),
    path('signup', auth_view.signup, name='signup'),
    path('logout', auth_view.logout_view)
]
