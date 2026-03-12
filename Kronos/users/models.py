from django.db import models

class UserType(models.Model):
    name = models.CharField(max_length=30)

class User(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    surname2 = models.CharField(max_length=30)
    email = models.EmailField()
    type = models.ForeignKey(
        UserType,
        on_delete=models.CASCADE,
        related_name='users'
    )

