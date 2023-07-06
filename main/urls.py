# -*- coding: utf-8 -*-
from django.urls import path
from . import apps, views

app_name = apps.AppConfig.name
urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('top/<int:year>/<int:month>/', views.TopView.as_view(), name='top'),
]
