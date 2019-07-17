# -*- coding: utf-8 -*-
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home-page'),
    path('profile/<str:username>/',
         views.ProfileView.as_view(),
         name='profile'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
