from django.db.models import Q
from rest_framework import serializers
from .models import User, Project, Task, UserProjectRole, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'image', 'username', 'first_name', 'last_name', 'email', 'password', 'projects', 'roles',
                  'tasks']
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
        return [
            {
               'project': task.project.title,
               'task': task.title
            }
            for task in Task.objects.filter(assigned_to=obj)
        ]

    @staticmethod
    def get_roles(obj):
        return [
            {
                'project': user_role.project.title,
                'role': user_role.role.name if user_role.role else None
            }
            for user_role in UserProjectRole.objects.filter(user=obj)
        ]


class UserProjectRoleSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserProjectRole
        fields = ['user', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'status', 'tasks', 'users']

    def create(self, validated_data):
        users_data = validated_data.pop('members', {})
        project = Project.objects.create(**validated_data)
        for user_data in users_data:
            user_id = user_data['user']
            role_id = user_data.get('role')
            UserProjectRole.objects.create(project=project, user_id=user_id, role_id=role_id)
        return project

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        users_data = validated_data.get('members', {})
        instance.save()
        for user_data in users_data:
            user_id = user_data['user']
            role_id = user_data.get('role')
            UserProjectRole.objects.update_or_create(project=instance, user_id=user_id, defaults={'role_id': role_id})
        return instance

    @staticmethod
    def get_tasks(obj):
        return [task.title for task in Task.objects.filter(project=obj)]

    @staticmethod
    def get_users(obj):
        return [
            {
                'user': f"{user_role.user.first_name} {user_role.user.last_name}",
                "role": RoleSerializer(user_role.role).data if user_role.role else None
            }
            for user_role in UserProjectRole.objects.filter(project=obj)
        ]


class TaskSerializer(serializers.ModelSerializer):
    tester = serializers.PrimaryKeyRelatedField(queryset=UserProjectRole.objects.filter(Q(role__name__icontains="тестировщик") | Q(role__name__icontains="Тестировщик")),
                                                allow_null=True)

    class Meta:
        model = Task
        fields = ['id', 'project', 'assigned_to', 'title', 'description', 'status', 'priority', 'created_at',
                  'updated_at', 'due_date', 'tester']

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
