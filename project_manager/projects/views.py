from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import ProjectSerializer, TaskSerializer, TimeTrackerSerializer
from .models import Project, Task, TimeTracker


@swagger_auto_schema(
    operation_description='Create a project',
    request_body=ProjectSerializer,
    responses={201: ProjectSerializer, 400: 'Bad Request'}
)
class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='List of projects',
        responses={200: ProjectSerializer, 400: 'Bad Request'}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Create a project',
        request_body=ProjectSerializer,
        responses={201: ProjectSerializer, 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'
    http_method_names = ['get', 'patch', 'delete']

    @swagger_auto_schema(
        operation_description='Retrieve a project',
        responses={200: ProjectSerializer, 404: 'Not Found'}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Update a project',
        request_body=ProjectSerializer,
        responses={200: ProjectSerializer, 400: 'Bad Request'}
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Delete a project',
        request_body=ProjectSerializer,
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='List of tasks',
        responses={200: TaskSerializer, 400: 'Bad Request'}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Create a task',
        request_body=TaskSerializer,
        responses={201: TaskSerializer, 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'
    http_method_names = ['get', 'patch', 'delete']

    @swagger_auto_schema(
        operation_description='Retrieve a task',
        responses={200: TaskSerializer, 404: 'Not Found'}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Update a task',
        request_body=TaskSerializer,
        responses={200: TaskSerializer, 400: 'Bad Request'}
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Delete a task',
        request_body=TaskSerializer,
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TimeTrackerView(generics.ListCreateAPIView):
    queryset = TimeTracker.objects.all()
    serializer_class = TimeTrackerSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='List of tasks with time trackers',
        responses={200: TimeTrackerSerializer, 400: 'Bad Request'}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Create a time tracker for a task in a project',
        request_body=TimeTrackerSerializer,
        responses={201: TimeTrackerSerializer, 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

