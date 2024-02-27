import pytest

from projects.models import Task, Project


class TestProjectApi:

    @pytest.mark.django_db
    def test_create_project(self, api_client, get_token):
        """ Test create project """
        data = {
              "title": "Project title",
              "description": "Project description",
              "team_members": [
                1,
                2
              ],
              "started_at": "2022-01-01T00:00:00Z",
              "finished_at": "2022-01-01T00:00:00Z"
        }
        response = api_client.post('/projects/', json=data,
                                   HTTP_AUTHORIZATION=f'Bearer {get_token["access"]}')
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_get_projects_list(self, api_client, get_token):
        """ Test get projects """
        response = api_client.get('/projects/',
                                  HTTP_AUTHORIZATION=f'Bearer {get_token["access"]}')
        assert response.status_code == 200
        assert len(response.data) == Project.objects.count()

    @pytest.mark.django_db
    def test_get_project_detail(self, api_client, get_token):
        """ Test get project detail """
        project = Project.objects.first()
        response = api_client.get(f'/projects/{project.id}/',
                                  HTTP_AUTHORIZATION=f'Bearer {get_token["access"]}')
        assert response.status_code == 200
        assert response.data['id'] == project.id
        assert response.data['title'] == project.title

    def test_get_projects_list_unauthorized(self, api_client):
        """ Test get projects without token """
        response = api_client.get('/projects/')
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_get_project_detail_unauthorized(self, api_client):
        """ Test get project detail without token """
        project = Project.objects.first()
        response = api_client.get(f'/projects/{project.id}/')
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_get_project_detail_not_found(self, api_client, get_token):
        """ Test get project detail not found """
        response = api_client.get(f'/projects/100/',
                                  HTTP_AUTHORIZATION=f'Bearer {get_token["access"]}')
        assert response.status_code == 404
        assert response.data['detail'] == 'Not found.'

    @pytest.mark.django_db
    def test_task_create(self, api_client, get_token):
        """ Test create task """
        project = Project.objects.first()
        data = {
            "title": "Task title",
            "description": "Task description",
            "own_project": project.id,
            "deadline": "2022-01-01T00:00:00Z",
            "assigned_to": [
                1,
            ]
        }
        response = api_client.post('/tasks/', json=data,
                                   HTTP_AUTHORIZATION=f'Bearer {get_token["access"]}')
        assert response.status_code == 201
        assert response.data['project'] == project.id
        assert response.data['title'] == data['title']

    @pytest.mark.django_db
    def test_get_task_detail(self, api_client, get_token):
        """ Test get task detail """
        task = Task.objects.first()
        response = api_client.get(f'/tasks/{task.id}/',
                                  HTTP_AUTHORIZATION=f'Bearer {get_token["access"]}')
        assert response.status_code == 200
        assert response.data['id'] == task.id
        assert response.data['title'] == task.title

    def test_task_create_unauthorized(self, api_client):
        """ Test create task without token """
        response = api_client.post('/tasks/')
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_start_time_tracking(self, api_client, get_token):
        """ Test start time treking """
        task = Task.objects.first()
        data = {
            "task": 1,
            "team_member": 1
        }
        response = api_client.post(f'/tasks/{task.id}', json=data,
                                   HTTP_AUTHORIZATION=f'Bearer {get_token["access"]}')
        assert response.status_code == 201

    def test_get_task_under_tracking(self, api_client, get_token):
        """ Test get task under tracking """
        response = api_client.get('/time-tracker/',
                                  HTTP_AUTHORIZATION=f'Bearer {get_token["access"]}')
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_delete_project(self, api_client, get_token):
        """ Test delete project """
        project = Project.objects.first()
        response = api_client.delete(f'/task/{project.id}/',
                                     HTTP_AUTHORIZATION=f'Bearer {get_token["access"]}')
        assert response.status_code == 204
        assert Project.objects.count() == 0






