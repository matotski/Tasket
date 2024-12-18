# Generated by Django 5.1.3 on 2024-11-16 14:08

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150)),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Активен"), ("archived", "Архивирован")],
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("username", models.CharField(max_length=150, unique=True)),
                ("first_name", models.CharField(max_length=150)),
                ("last_name", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254)),
                (
                    "role",
                    models.CharField(
                        choices=[
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
                        ],
                        max_length=150,
                    ),
                ),
                ("password", models.CharField(max_length=200)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default="users_image/avatar.png",
                        null=True,
                        upload_to="users_image",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150)),
                ("description", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("grooming", "Grooming"),
                            ("in_progress", "In Progress"),
                            ("dev", "Dev"),
                            ("done", "Done"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("low", "Низкий"),
                            ("medium", "Средний"),
                            ("high", "Высокий"),
                        ],
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("due_date", models.DateTimeField()),
                (
                    "assigned_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.project"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProjectRole",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
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
                        ],
                        max_length=150,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.project"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="project",
            name="users",
            field=models.ManyToManyField(
                through="users.UserProjectRole", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
