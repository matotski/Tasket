# Generated by Django 5.1.3 on 2024-11-17 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='users',
            new_name='users_with_roles',
        ),
    ]
