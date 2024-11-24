from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    image = models.ImageField(upload_to="users_image", default='users_image/avatar.png', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Project(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50,
                              choices=[
                                  ('active', 'Активен'),
                                  ('archived', 'Архивирован')
                              ])
    users = models.ManyToManyField(User, through='UserProjectRole')

    def __str__(self):
        return f"{self.title}"


class Role(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class UserProjectRole(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    role = models.ForeignKey(to=Role, max_length=150, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.role}"


class Task(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    status = models.CharField(max_length=50,
                              choices=[
                                  ('grooming', 'Grooming'),
                                  ('in_progress', 'In Progress'),
                                  ('dev', 'Dev'),
                                  ('done', 'Done')
                              ])
    priority = models.CharField(max_length=20,
                                choices=[
                                    ('low', 'Низкий'),
                                    ('medium', 'Средний'),
                                    ('high', 'Высокий')
                                ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()
    tester = models.ForeignKey(to=UserProjectRole, on_delete=models.SET_NULL, blank=True, null=True)



    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
