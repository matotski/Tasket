from rest_framework import serializers
from .models import User, Project, Task, UserProjectRole


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()
    roles_in_projects = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'roles_in_projects', 'password', 'image', 'projects', 'tasks']
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

    @staticmethod
    def get_roles_in_projects(obj):
        return [
            {
                'project': user_role.project.title,
                'role': user_role.role
            }
            for user_role in UserProjectRole.objects.filter(user=obj)
        ]


class ProjectSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()
    users_with_roles = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'status', 'tasks', 'users_with_roles']

    def create(self, validated_data):
        users_data = validated_data.pop('users_with_roles', [])
        project = Project.objects.create(**validated_data)
        for user_data in users_data:
            user = User.objects.get(id=user_data['user'])
            role = user_data['role']
            UserProjectRole.objects.create(project=project,user=user,role=role)
        return project

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        users_data = validated_data.get('users_with_roles', [])
        instance.save()
        if users_data:
            instance.userprojectrole_set.all().delete()
            for user_data in users_data:
                user = user_data['user']
                role = user_data['role']
                UserProjectRole.objects.create(project=instance, user=user, role=role)
        return instance

    @staticmethod
    def get_tasks(obj):
        return [task.title for task in Task.objects.filter(project=obj)]

    @staticmethod
    def get_users_with_roles(obj):
        return [
            {
                'user': user_role.user.username,
                'role': user_role.role
            }
        for user_role in UserProjectRole.objects.filter(project=obj)
        ]


class UserProjectRoleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'project', 'user', 'role']

    def create(self, validated_data):
        return UserProjectRole.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'project', 'assigned_to', 'title', 'description', 'status', 'priority', 'created_at', 'updated_at', 'due_date']

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.project = validated_data.get('project', instance.project)
        instance.assigned_to = validated_data.get('assigned_to', instance.assigned_to)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.save()
        return instance


