from django.test import TestCase
from todo.models import Task
from rest_framework import status
from api_v1.serializers import TaskSerializer
import json
class TestUrlTodoIsAlive(TestCase):
    def test_index(self):
        resp = self.client.get('http://localhost:8000/todo-list/')
        self.assertEqual(resp.status_code,200)


class TestGetTasksSucess(TestCase):
    def setUp(self):
        for i in range(1,3):
            Task.objects.create(description='tasks {}'.format(i))

    def test_index(self):
        
        response = self.client.get('http://localhost:8000/todo-list/api/v1/tasks/')
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

class TestCreateTasksSucess(TestCase):
    
    def test_index(self):
        data = {'description': 'tasks'}
        response = self.client.post('http://localhost:8000/todo-list/api/v1/tasks/', data=data)
        tasks = Task.objects.get(description='tasks')
        serializer = TaskSerializer(tasks)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

class TestRenameTasksSucess(TestCase):
    def setUp(self):
        self.create_task = Task.objects.create(description='tasks created')
        
    def test_index(self):
        data = {"description": "tasks rename"}
        url = 'http://localhost:8000/todo-list/api/v1/tasks/{}/'.format(self.create_task.id)
        
        response = self.client.put( url, data=json.dumps(data), content_type='application/json')
        tasks = Task.objects.get(description='tasks rename')
        serializer = TaskSerializer(self.create_task)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('description'), data['description'])