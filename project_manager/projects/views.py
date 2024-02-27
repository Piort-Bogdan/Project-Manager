from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import ProjectSerializer, TaskSerializer, TimeTrackerSerializer, ProjectErrorSerializer
from .models import Project, Task, TimeTracker


class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'started_at', 'finished_at', 'team_members']

    @extend_schema(
        description='List all projects',
        responses={200: ProjectSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        description='Create a new project',
        request=ProjectSerializer,
        responses={201: ProjectSerializer},
        examples=[
            OpenApiExample('Example 1', summary='Create a project', value={
                'title': 'Project title', 'description': 'Project description', 'team_members': [1, 2],
                'started_at': '2022-01-01T00:00:00Z', 'finished_at': '2022-01-01T00:00:00Z'}),
        ],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = []
    # permission_classes = [IsAdminUser]
    lookup_field = 'id'
    http_method_names = ['get', 'patch', 'delete']

    @extend_schema(
        description='Retrieve a project details',
        responses={200: ProjectSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        description='Update a project details',
        request=ProjectSerializer,
        responses={200: ProjectSerializer, 400: ProjectErrorSerializer},
        examples=[
            OpenApiExample('Example 1', summary='Update a project', value={
                'title': 'Project title', 'description': 'Project description', 'team_members': [1, 2],
                'started_at': '2022-01-01T00:00:00Z', 'finished_at': '2022-01-01T00:00:00Z'}),
        ],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        description='Delete a project',
        responses={204: ProjectErrorSerializer},
        examples=[
            OpenApiExample('Example 1', summary='Delete a project', value={'id': '1'}),
        ]
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['deadline', 'assigned_to', 'own_project', 'status', 'title']

    @extend_schema(
        description='List all tasks',
        responses={200: TaskSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        description='Create a new task',
        request=TaskSerializer,
        responses={201: TaskSerializer},
        examples=[
            OpenApiExample('Example 1', summary='Create a task', value={
                'title': 'Task title', 'description': 'Task description', 'deadline': '2022-01-01T00:00:00Z',
                'own_project': 1, 'assigned_to': [1, 2]}),
        ],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'
    http_method_names = ['get', 'patch', 'delete']

    @extend_schema(
        description='Retrieve a task details',
        responses={200: TaskSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        description='Update a task details',
        request=TaskSerializer,
        responses={200: TaskSerializer},
        examples=[
            OpenApiExample('Example 1', summary='Update a task', value={
                'title': 'Task title', 'description': 'Task description', 'deadline': '2022-01-01T00:00:00Z',
                'own_project': 1, 'assigned_to': [1, 2]}),
        ],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        description='Delete a task',
        responses={204: TaskSerializer},
        examples=[
            OpenApiExample('Example 1', summary='Delete a task', value={'id': '1'}),
        ]
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TimeTrackerView(generics.ListCreateAPIView):
    queryset = TimeTracker.objects.all()
    serializer_class = TimeTrackerSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description='List all time trackers',
        responses={200: TimeTrackerSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        description='Create a new time tracker',
        request=TimeTrackerSerializer,
        responses={201: TimeTrackerSerializer},
        examples=[
            OpenApiExample('Example 1', summary='Create a time tracker', value={
                'task': 1, 'team_member': 1}),
        ],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
