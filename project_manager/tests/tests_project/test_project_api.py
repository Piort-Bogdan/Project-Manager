from rest_framework import status

from tests.test_setup import TestSetUp


class TestProjectApi(TestSetUp):

    def test_create_project(self):
        """ Test create project """
        data = {
            "title": "Project title",
            "description": "Project description",
            "team_members": [
                self.user.objects.all().first().id,
            ],
            "started_at": "2022-01-01T00:00:00Z",
            "finished_at": "2022-01-01T00:00:00Z"
        }
        response = self.client.post(self.projects_url, data=data,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_projects_list(self):
        """ Test get projects """
        response = self.client.get(self.projects_url,
                                   HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        assert response.status_code == 200

    def test_get_project_detail(self):
        """ Test get project detail """
        response = self.client.get(self.projects_det_url, {'id': self.project.id},
                                   HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_projects_list_unauthorized(self):
        """ Test get projects without token """
        response = self.client.get(self.projects_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_project_detail_not_found(self):
        """ Test get project detail not found """
        response = self.client.get(self.get_detail_url('project-detail', 1000),
                                   HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_create(self):
        """ Test create task """
        data = {
            "title": "Task title",
            "description": "Task description",
            "own_project": self.project.id,
            "deadline": "2022-01-01T00:00:00Z",
            "assigned_to": [
                self.user.objects.all().first().id,
            ]
        }
        response = self.client.post(self.task_url, data=data,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_task_detail(self):
        """ Test get task detail """
        response = self.client.get(self.task_det_url, {'id': self.task.id},
                                   HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_create_unauthorized(self):
        """ Test create task without token """
        data = {
            "title": "Task title",
            "description": "Task description",
            "own_project": self.project.id,
            "deadline": "2022-01-01T00:00:00Z",
            "assigned_to": [
                self.user.objects.all().first().id,
            ]
        }
        response = self.client.post(self.task_url, json=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_start_time_tracking(self):
        """ Test start time tracking """
        task = self.get_task()
        data = {
            "task": task.id,
            "team_member": self.user.objects.all().last().id
        }
        response = self.client.post(self.time_tracker_url, data=data,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_task_under_tracking(self):
        """ Test get task under tracking """
        response = self.client.get(self.time_tracker_url,
                                   HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_project(self):
        """ Test delete project """
        response = self.client.delete(self.projects_det_url,
                                      HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
