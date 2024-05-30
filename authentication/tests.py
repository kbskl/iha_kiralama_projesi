import random

from django.contrib.auth.models import User
from django.test import TestCase

from user.models import Profile


class AuthenticationTests(TestCase):
    def setUp(self):
        self.username = f"testuser_{random.randint(1, 99999)}"
        self.first_name = "test_first_name"
        self.last_name = "test_last_name"
        User.objects.create_user(self.username, password=self.username, first_name=self.first_name,
                                 last_name=self.last_name)

    def test_user_creation(self):
        user = User.objects.get(username=self.username)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)

    def test_user_profile(self):
        user = User.objects.get(username=self.username)
        profile = Profile.objects.get(user=user)
        self.assertEqual(user, profile.user)
