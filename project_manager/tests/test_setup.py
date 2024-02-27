from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from projects.models import Project, Task, TimeTracker


class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.projects_url = reverse('project-list')

        self.task_url = reverse('task-list')

        self.time_tracker_url = reverse('time-tracker')
        self.message_url = reverse('message-list')

        self.client = APIClient()

        self.token, self.user = self.get_token()
        self.project = self.get_project()
        self.task = self.get_task()
        self.tracker = self.get_time_tracker()

        self.projects_det_url = self.get_detail_url('project-detail', self.project.id)
        self.task_det_url = self.get_detail_url('task-detail', self.task.id)

        return super().setUp()

    def get_token(self) -> tuple:
        user_model = get_user_model()
        user_model.objects.create_user(username='admin', email='admin@example.com', password='admin',
                                       is_superuser=True, is_staff=True)
        resp = self.client.post(self.login_url, {'username': 'admin', 'password': 'admin'})
        return resp.data, user_model

    def get_project(self):
        project = Project.objects.create(title='Project title',
                                         description='Project description',
                                         started_at='2022-01-01T00:00:00Z',
                                         finished_at='2022-01-01T00:00:00Z',
                                         )
        project.team_members.set(self.user.objects.all())
        return project

    def get_task(self):
        task = Task.objects.create(title='Task title',
                                   description='Task description',
                                   own_project=self.project,
                                   deadline='2022-01-01T00:00:00Z',
                                   )
        task.assigned_to.set(self.user.objects.all())
        return task

    def get_time_tracker(self):
        tracker = TimeTracker.objects.create(task=self.task,
                                             team_member=self.user.objects.all().first(),
                                             )
        return tracker

    @staticmethod
    def get_detail_url(url: str, _id: int) -> str:
        return reverse(url, args=[_id])

    def tearDown(self):
        return super().tearDown()
