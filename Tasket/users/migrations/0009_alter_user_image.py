# Generated by Django 5.1.3 on 2024-11-13 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_task_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='users_image/avatar.png', null=True, upload_to='users_image'),
        ),
    ]
