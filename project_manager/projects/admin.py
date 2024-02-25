from django.contrib import admin

from .models import Project, Task, TimeTracker

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TimeTracker)

