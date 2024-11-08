from django.db import models
from django.contrib.auth.models import AbstractUser


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()

    def __str__(self):
        return f"{self.title}"


class Task(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"


class User(AbstractUser):
    CHOICES = {
        "Admin": "Администратор",
        "PM1": "Менеджер проекта",
        "PM2": "Старший менеджер проекта",
        "EMP1": "Сотрудник",
        "EMP2": "Старший сотрудник",
        "DATA1": "Аналититк",
        "DATA2": "Старший аналитик",
        "DES1": "Дизайнер",
        "DES2": "Старший дизайнер",
        "DEV1": "Разработчик",
        "DEV2": "Старший разработчик",
        "QA1": "Тестировщик",
        "QA2": "Старший тестировщик",
    }
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    role = models.CharField(max_length=50, choices=CHOICES)
    password = models.CharField(max_length=70)
    image = models.ImageField(upload_to="users_image", null=True, blank=True)
    ongoing_projects = models.ManyToManyField(Project)
    ongoing_tasks = models.ManyToManyField(Task)

    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.role}"
