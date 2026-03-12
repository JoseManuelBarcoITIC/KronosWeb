
from django.urls import path
from . import views


urlpatterns = [
    path("", views.getAllUsers, name="userList"),

]
