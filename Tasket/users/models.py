from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    role = models.CharField(max_length=50)
    password = models.CharField(max_length=70)
    image = models.ImageField(upload_to="users_image", null=True, blank=True)
    ongoing_projects = models.CharField(max_length=200)
    history_of_projects = models.CharField(max_length=200)
