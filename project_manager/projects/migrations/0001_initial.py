# Generated by Django 4.2.10 on 2024-02-27 21:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('started_at', models.DateTimeField()),
                ('finished_at', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('team_members', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-started_at'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('deadline', models.DateTimeField()),
                ('status', models.SmallIntegerField(choices=[(1, 'In progress'), (2, 'Completed'), (3, 'Delayed'), (4, 'Just created')], default=4)),
                ('is_active', models.BooleanField(default=True)),
                ('assigned_to', models.ManyToManyField(blank=True, related_name='tasks', to=settings.AUTH_USER_MODEL)),
                ('own_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects.project')),
            ],
            options={
                'ordering': ['-deadline'],
            },
        ),
        migrations.CreateModel(
            name='TimeTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('time_spent', models.DurationField(blank=True, null=True)),
                ('paused_at', models.DateTimeField(blank=True, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.task')),
                ('team_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-ended_at'],
                'unique_together': {('task', 'team_member')},
            },
        ),
    ]
