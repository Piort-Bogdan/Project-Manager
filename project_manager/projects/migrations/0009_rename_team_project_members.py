# Generated by Django 5.0.2 on 2024-02-24 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_task_assigned_to_delete_team'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='team',
            new_name='members',
        ),
    ]