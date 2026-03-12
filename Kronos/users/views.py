from django.shortcuts import render

from .models import User


# Create your views here.
def getAllUsers(request):
    allUsers = User.objects.all()
    response = {"users":allUsers}
    return render(request, 'users_main_page.html',response)
