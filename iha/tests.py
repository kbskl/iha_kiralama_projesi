import random

from django.contrib.auth.models import User
from django.test import TestCase

from iha.models import IHA


class IHATests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(f'testuser_{random.randint(0, 9999)}',
                                             password=f"{random.randint(9999999, 999999999)}")
        self.title = "test title"
        self.brand = "test brand"
        self.model = "test model"
        self.uuid = IHA.objects.create(title=self.title, brand=self.brand, model=self.model, owner=self.user).uuid

    def test_fields(self):
        iha = IHA.objects.filter(uuid=self.uuid).first()
        self.assertEqual(iha.title, self.title.title())
        self.assertEqual(iha.brand, self.brand.title())
        self.assertEqual(iha.model, self.model.title())

    def test_unanswered_request(self):
        iha = IHA.objects.filter(uuid=self.uuid).first()
        self.assertEqual(iha.check_unanswered_request(), 0)
