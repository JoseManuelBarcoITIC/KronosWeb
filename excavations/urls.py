
from django.contrib import admin
from . import views

from django.urls import path,include


urlpatterns = [
    path('excavations/', views.excavation_list, name='excavation-list'),
    path('excavations/<int:pk>/', views.excavation_detail, name='excavation-detail'),

    path('sectors/', views.sector_list, name='sector-list'),
    path('sectors/<int:pk>/', views.sector_detail, name='sector-detail'),
]