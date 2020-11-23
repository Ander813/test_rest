from datetime import date

from django.contrib.auth.hashers import check_password
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from task_list.models import User, Task


class TasksTests(APITestCase):
    def test_create_account(self):
        url = reverse('register')
        data = {'email': 'some_email@mail.ru',
                'password': 'Qwerty123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(id=1).email, data['email'])
        self.assertEqual(check_password(data['password'], User.objects.get(id=1).password), True)
        user = User.objects.get(id=1)
        token = Token.objects.get(user=user).key

    def test_login_account(self):
        url = reverse('login')
        user = User.objects.create_user(email='some_email@mail.ru', password='Qwerty123')
        data = {'email': 'some_email@mail.ru',
                'password': 'Qwerty123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = Token.objects.get(user=user).key
        self.assertEqual(response.data['token'], token)

    def test_task_create(self):
        user = User.objects.create_user(email='some_email@mail.ru', password='Qwerty123')
        token = Token.objects.get(user_id=1).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        url = reverse('task_create')
        data = {'title': 'a',
                'text': 'b',
                'complete_date': '2020-12-31'}
        expected_response_data = {
                "title": "a",
                "text": "b",
                "complete_date": "2020-12-31",
                "completed": False
                }
        response = self.client.post(url,
                                    data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_response_data, response.data)
        self.assertEqual(Task.objects.get(id=1).title, expected_response_data['title'])
        self.assertEqual(Task.objects.get(id=1).text, expected_response_data['text'])
        self.assertEqual(Task.objects.get(id=1).complete_date, date(2020, 12, 31))
        self.assertEqual(Task.objects.get(id=1).completed, expected_response_data['completed'])

    def test_task_list(self):
        url = reverse('task_create')
        user = User.objects.create_user(email='some_email@mail.ru', password='Qwerty123')
        token = Token.objects.get(user=user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        data = [{'title': 'a',
                 'text': 'b',
                 'complete_date': '2020-12-31'},
                {'title': 'c',
                 'text': 'd',
                 'complete_date': '2020-12-30'}]
        expected_response_data = [{'title': 'a',
                                   'text': 'b',
                                   'complete_date': '2020-12-31',
                                   'completed': False},
                                  {'title': 'c',
                                   'text': 'd',
                                   'complete_date': '2020-12-30',
                                   'completed': False}]
        self.client.post(url, data[0], format='json')
        self.client.post(url, data[1], format='json')
        tasks = []
        tasks.append(Task.objects.get(id=1))
        tasks.append(Task.objects.get(id=2))
        url = reverse('tasks')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for task_ind in range(len(response.data)):
            self.assertEqual(dict(response.data[task_ind]), expected_response_data[task_ind])

    def test_task_delete(self):
        url = reverse('tasks')
        user = User.objects.create_user(email='some_email@mail.ru', password='Qwerty123')
        token = Token.objects.get(user=user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        data = {'title': 'a',
                'text': 'b',
                'complete_date': '2020-12-31'}
        self.client.post(url, data, format='json')
        url = reverse('task', kwargs={'pk': 1})
        self.client.delete(url)
        self.assertFalse(Task.objects.filter(id=1))

    def test_task_completed(self):
        url = reverse('task_create')
        user = User.objects.create_user(email='some_email@mail.ru', password='Qwerty123')
        token = Token.objects.get(user=user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        data = {'title': 'a',
                'text': 'b',
                'complete_date': '2020-12-31'}
        expected_response_data = {'title': 'a',
                                  'text': 'b',
                                  'complete_date': '2020-12-31',
                                  'completed': True}
        self.client.post(url, data, format='json')
        url = reverse('task', kwargs={'pk': 1})
        response = self.client.patch(url, {'completed': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response_data)

    def test_task_get(self):
        url = reverse('task_create')
        user = User.objects.create_user(email='some_email@mail.ru', password='Qwerty123')
        token = Token.objects.get(user=user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        data = {'title': 'a',
                'text': 'b',
                'complete_date': '2020-12-31'}
        expected_response_data = {'title': 'a',
                                  'text': 'b',
                                  'complete_date': '2020-12-31',
                                  'completed': False}
        self.client.post(url, data, format='json')
        url = reverse('task', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response_data)




