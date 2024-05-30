from django.contrib.auth.models import User
from django.db import models

from general_util.constant import GenderEnum
from general_util.model import GeneralModel


class Profile(GeneralModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(choices=GenderEnum.choices(), verbose_name='Cinsiyet', blank=True, null=True,
                              max_length=20)

    def __str__(self):
        return self.user.username
