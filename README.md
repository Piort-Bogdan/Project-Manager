## Project management tool

This is a simple project management tool that allows you to create, read, update and delete projects and tasks. It is built using Django and Django Rest Framework.

120 characters per line choised for this project.

### Installation
First of all, need to specify docker-config.env file according to docker-config.example.env file.
(To save time on creating the production env file right there)

#### Then, build the docker image by running the following command:
```shell
docker-compose build
```
#### Then, run the following command to start the server:
```shell
docker-compose up
```

### Testing
To run the tests, run the following command:
```shell
docker-compose --profile test up --abort-on-container-exit --exit-code-from backend_test
```
Flake8 and pytest checks:
```shell
pytest && flake8 --ignore=E501 .

```

### Usage
Using the API you can create, read, update and delete projects and tasks. You can also filter the projects and tasks by their status and due date.
You can also track the time spent on each task.
To get JWT token, you need to register and then login to the system.
After that, you can use the token to access the API.

### Documentation
The API documentation can be found at the following link:
[API Documentation](http://localhost:8000/api/docs/)