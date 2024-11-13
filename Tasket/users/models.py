from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField


class User(AbstractUser):
    CHOICES = [
        ("Admin", "Администратор"),
        ("PM1", "Менеджер проекта"),
        ("PM2", "Старший менеджер проекта"),
        ("EMP1", "Сотрудник"),
        ("EMP2", "Старший сотрудник"),
        ("DATA1", "Аналитик"),
        ("DATA2", "Старший аналитик"),
        ("DES1", "Дизайнер"),
        ("DES2", "Старший дизайнер"),
        ("DEV1", "Разработчик"),
        ("DEV2", "Старший разработчик"),
        ("QA1", "Тестировщик"),
        ("QA2", "Старший тестировщик"),
    ]
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    role = models.CharField(max_length=150, choices=CHOICES)
    password = models.CharField(max_length=200)
    image = models.ImageField(upload_to="users_image", default='users_image/avatar.png', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.role}"


class Project(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    deadline = models.DateTimeField()
    users = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.title}"


class Task(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"
