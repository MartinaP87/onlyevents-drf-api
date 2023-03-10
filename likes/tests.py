from django.contrib.auth.models import User
from .models import Like
from comments.models import Comment
from events.models import Event
from categories.models import Category
from rest_framework import status
from rest_framework.test import APITestCase


class LikeListViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_user(username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')
        music = Category.objects.create(cat_name='music')
        event = Event.objects.create(
            owner=marla, title='a title', category=music,
            date='2020-11-28T19:24:58.478641+05:30', location='a location',
            address='an address')
        Comment.objects.create(owner=marla, posted_event=event)

    def test_can_list_likes(self):
        marla = User.objects.get(username='marla')
        comment = Comment.objects.get(pk=1)
        Like.objects.create(owner=marla, comment=comment)
        response = self.client.get('/likes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_a_like_instance(self):
        comment = Comment.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.post(
            '/likes/', {'comment': comment.id})
        count = Like.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_a_like_instance(self):
        comment = Comment.objects.get(pk=1)
        response = self.client.post(
            '/likes/', {'comment': comment.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LikeDetailViewTests(APITestCase):
    def setUp(self):
        marla = User.objects.create_user(username='marla', password='pass')
        peter = User.objects.create_user(username='peter', password='pass')
        music = Category.objects.create(cat_name='music')
        event = Event.objects.create(
            owner=marla, title='a title', category=music,
            date='2020-11-28T19:24:58.478641+05:30', location='a location',
            address='an address')
        comment = Comment.objects.create(owner=marla, posted_event=event)
        like1 = Like.objects.create(owner=marla, comment=comment)
        like2 = Like.objects.create(owner=peter, comment=comment)

    def test_can_retrieve_like_instance_using_valid_id(self):
        response = self.client.get('/likes/1/')
        self.assertEqual(response.data['owner'], 'marla')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_like_instance_using_invalid_id(self):
        response = self.client.get('/likes/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_delete_own_like_instance(self):
        like1 = Like.objects.get(pk=1)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/likes/1/')
        response2 = self.client.get('likes/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cant_delete_someone_else_like_instance(self):
        like2 = Like.objects.get(pk=2)
        self.client.login(username='marla', password='pass')
        response = self.client.delete('/likes/2/')
        response2 = self.client.get('/likes/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
