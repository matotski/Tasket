from rest_framework import serializers
from .models import User, Project, Task


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'password', 'image', 'projects', 'tasks']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

    @staticmethod
    def get_projects(obj):
        return [project.title for project in Project.objects.filter(users=obj)]

    @staticmethod
    def get_tasks(obj):
        return [task.title for task in Task.objects.filter(assigned_to=obj)]


class ProjectSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'deadline','tasks', 'users']

    def create(self, validated_data):
        users_data = validated_data.pop('users', [])
        project = Project.objects.create(**validated_data)
        project.users.set(users_data)
        return project

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        users_data = validated_data.get('users', instance.users)
        if users_data is not None:
            instance.users.set(users_data)
        instance.save()
        return instance

    @staticmethod
    def get_tasks(obj):
        return [task.title for task in Task.objects.filter(project=obj)]

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'project', 'assigned_to', 'title', 'description', 'is_completed']

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.project = validated_data.get('project', instance.project)
        instance.assigned_to = validated_data.get('assigned_to', instance.assigned_to)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.is_completed = validated_data.get('is_completed', instance.is_completed)
        instance.save()
        return instance
