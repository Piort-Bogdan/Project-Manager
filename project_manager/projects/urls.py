from django.urls import path
from .views import (ProjectListView, ProjectDetailView,
                    TaskListView, TaskDetailView, TimeTrackerView)

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:id>', ProjectDetailView.as_view(), name='project-detail'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:id>', TaskDetailView.as_view(), name='task-detail'),
    path('time-tracker/', TimeTrackerView.as_view(), name='time-tracker'),
]