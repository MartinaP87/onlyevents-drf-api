from django.contrib.auth.models import User
from .models import Going
from events.models import Event
from categories.models import Category
from rest_framework import status
from rest_framework.test import APITestCase


class GoingListViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_user(username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')
        music = Category.objects.create(cat_name='music')
        Event.objects.create(
            owner=marla, title='a title', category=music,
            date='2020-11-28T19:24:58.478641+05:30', location='a location',
            address='an address')

    def test_can_list_goings(self):
        marla = User.objects.get(username='marla')
        event = Event.objects.get(pk=1)
        Going.objects.create(owner=marla, posted_event=event)
        response = self.client.get('/going/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_a_going_instance(self):
        event = Event.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.post(
            '/going/', {'posted_event': event.id})
        count = Going.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_a_going_instance(self):
        event = Event.objects.get(pk=1)
        response = self.client.post(
            '/going/', {'posted_event': event.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GoingDetailViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_user(username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')
        music = Category.objects.create(cat_name='music')
        event1 = Event.objects.create(
            owner=marla, title='a title', category=music,
            date='2020-11-28T19:24:58.478641+05:30', location='a location',
            address='an address')
        event2 = Event.objects.create(
            owner=peter, title='a different title', category=music,
            date='2020-11-18T19:24:58.478641+05:30', location='a location',
            address='an address')
        going1 = Going.objects.create(owner=marla, posted_event=event1)
        going2 = Going.objects.create(owner=peter, posted_event=event2)

    def test_can_retrieve_going_instance_using_valid_id(self):
        response = self.client.get('/going/1/')
        self.assertEqual(response.data['owner'], 'marla')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_going_instance_using_invalid_id(self):
        response = self.client.get('/going/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_delete_own_going_instance(self):
        going1 = Going.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/going/1/')
        response2 = self.client.get('going/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cant_delete_someone_else_going_instance(self):
        going2 = Going.objects.get(pk=2)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/going/2/')
        response2 = self.client.get('/going/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
