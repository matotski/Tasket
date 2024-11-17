from django.forms import model_to_dict
from django.shortcuts import render
from .models import User, Project, Task, UserProjectRole
from rest_framework import viewsets
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, UserProjectRoleSerializer


# def index(request):
#     context = {
#         "users": User.objects.all(),
#         "projects": Project.objects.all(),
#         "tasks": Task.objects.all()
#     }
#     return render(request, 'index.html', context=context)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProjectRoleViewSet(viewsets.ModelViewSet):
    queryset = UserProjectRole.objects.all()
    serializer_class = UserProjectRoleSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
