from django.urls import path
from . import views
from .views import MyTokenObtainPairView


urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('userlist/', views.users_list, name='users_list'),
    path('<int:pk>/', views.user_detail, name='user_detail'),
]