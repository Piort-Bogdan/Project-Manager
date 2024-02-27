# Generated by Django 5.0.2 on 2024-02-24 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.IntegerField(choices=[(1, 'In progress'), (2, 'Completed'), (3, 'Delayed'), (4, 'Just created')], default=4),
        ),
    ]
