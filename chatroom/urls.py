# -*- coding: utf-8 -*-
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(r'', views.IndexView.as_view(), name='home-page'),
    path(r'profile/', views.IndexView.as_view(), name='profile'),
    # Auth
    path(r'register/', views.register, name='register'),
    path(r'login/', auth_views.LoginView.as_view(), name='login'),
    path(r'logout/', auth_views.LogoutView.as_view(), name='logout'),
]
