from datetime import date

from django.contrib.auth.hashers import check_password
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from task_list.models import User, Task


class AuthorizationTests(APITestCase):
    data = {'email': 'some_email@mail.ru',
            'password': 'Qwerty123'}

    def test_create_account(self):
        url = reverse('register')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(id=1).email, self.data['email'])
        self.assertEqual(check_password(self.data['password'], User.objects.get(id=1).password), True)
        user = User.objects.get(id=1)
        token = Token.objects.get(user=user).key

    def test_login_account(self):
        url = reverse('login')
        user = User.objects.create_user(email=self.data['email'], password=self.data['password'])
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = Token.objects.get(user=user).key
        self.assertEqual(response.data['token'], token)


class TasksTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='some_email@mail.ru', password='Qwerty123')
        self.token = Token.objects.get(user_id=1).key

        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_task_create(self):
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

        self.client.force_authenticate(user=None)
        response = self.client.post(url,
                                    data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_task_list(self):
        url = reverse('task_create')
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

        self.client.force_authenticate(user=None)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_task_delete(self):
        url = reverse('tasks')
        data = {'title': 'a',
                'text': 'b',
                'complete_date': '2020-12-31'}
        self.client.post(url, data, format='json')
        url = reverse('task', kwargs={'pk': 1})
        self.client.delete(url)
        self.assertFalse(Task.objects.filter(id=1))

    def test_task_completed(self):
        url = reverse('task_create')
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

        self.client.force_authenticate(user=None)
        response = self.client.patch(url, {'completed': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_task_get(self):
        url = reverse('task_create')
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

        self.client.force_authenticate(user=None)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)





