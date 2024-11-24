from django.forms import model_to_dict
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import User, Project, Task, UserProjectRole, Role, Comment
from rest_framework import viewsets, status
from rest_framework import filters as drf_filters
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, UserProjectRoleSerializer, RoleSerializer, CommentSerializer
from .filters import TaskFilter
from django_filters import rest_framework as filters


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


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['created_at']


class UserProjectRoleViewSet(viewsets.ModelViewSet):
    queryset = UserProjectRole.objects.all()
    serializer_class = UserProjectRoleSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        return self.queryset.filter(project_id=project_id)

    def create(self, request, project_pk=None):
        project = Project.objects.get(pk=project_pk)
        user_id = request.data.get('user')
        role_id = request.data.get('role')
        user = User.objects.get(pk=user_id)
        role = Role.objects.get(pk=role_id) if role_id else None
        user_project_role = UserProjectRole.objects.create(
            project=project,
            user=user,
            role=role
        )
        return Response(self.get_serializer(user_project_role).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, project_pk=None, pk=None):
        try:
            user_project_role = self.get_queryset().get(pk=pk)
            user_project_role.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserProjectRole.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        return self.queryset.filter(project_id=project_id)

    def create(self, request, project_pk=None):
        if not Project.objects.filter(pk=project_pk).exists():
            return Response({"error": "Project does not exist."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(project_id=project_pk)
        return Response(self.get_serializer(task).data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        task_id = self.kwargs.get('task_pk')
        return self.queryset.filter(task_id=task_id)

    def create(self, request, project_pk=None,task_pk=None):
        if not Task.objects.filter(pk=task_pk, project_id=project_pk).exists():
            return Response({"error": "Task does not exist in this project."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(task_id=task_pk)
        return Response(self.get_serializer(comment).data, status=status.HTTP_201_CREATED)

