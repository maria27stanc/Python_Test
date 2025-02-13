from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_weather, name='get_weather'),
    path('location_data/', views.location_data, name='location_data'),
]
# -*- coding: utf-8 -*-

