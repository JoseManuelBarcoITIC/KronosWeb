
from django.contrib import admin
from . import views

from django.urls import path,include



urlpatterns = [
    path('userlist/', views.excavation_list, name='users_list'),
]
