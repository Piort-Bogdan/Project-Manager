import datetime

from django.db import models


class Project(models.Model):
    """ Model for creating projects"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    team_members = models.ManyToManyField('auth.User', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Task(models.Model):

    STATUS = (
        (1, 'In progress'),
        (2, 'Completed'),
        (3, 'Delayed'),
        (4, 'Just created'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    own_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    status = models.SmallIntegerField(choices=STATUS, default=4)
    assigned_to = models.ManyToManyField('auth.User', blank=True, related_name='tasks')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class TimeTracker(models.Model):
    """ Model for tracking time"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    team_member = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    start_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    time_spent = models.DurationField(blank=True, null=True)
    paused_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['task', 'team_member']
