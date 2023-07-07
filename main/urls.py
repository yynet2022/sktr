# -*- coding: utf-8 -*-
from django.urls import path
from . import apps, views

app_name = apps.AppConfig.name
urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('top/<int:year>/<int:month>/', views.TopView.as_view(), name='top'),
    path('reserve/<uuid:seatid>/<int:year>-<int:month>-<int:day>/',
         views.ReserveView.as_view(), name='reserve'),
    path('cancel/<int:year>-<int:month>-<int:day>/',
         views.CancelView.as_view(), name='cancel'),
]
