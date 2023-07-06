# -*- coding: utf-8 -*-
from django.urls import path
from . import apps, views

app_name = apps.AppConfig.name
urlpatterns = [
    # path('', views.index, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView, name='logout'),
]
