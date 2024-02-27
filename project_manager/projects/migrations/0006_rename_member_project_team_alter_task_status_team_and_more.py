# Generated by Django 5.0.2 on 2024-02-24 19:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_task_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='member',
            new_name='team',
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'In progress'), (2, 'Completed'), (3, 'Delayed'), (4, 'Just created')], default=4),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('member', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_to',
            field=models.ManyToManyField(related_name='tasks', to='projects.team'),
        ),
    ]