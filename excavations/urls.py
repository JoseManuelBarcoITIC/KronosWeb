from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('excavations/', views.excavation_list, name='excavation-list'),
    path('excavations/<int:pk>/', views.excavation_detail, name='excavation-detail'),

    path('sectors/', views.sector_list, name='sector-list'),
    path('sectors/<int:pk>/', views.sector_detail, name='sector-detail'),

    path('stratigraphic-units/', views.stratigraphic_unit_list, name='stratigraphic-unit-list'),
    path('stratigraphic-units/<int:pk>/', views.stratigraphic_unit_detail, name='stratigraphic-unit-detail'),
]