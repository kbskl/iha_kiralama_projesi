from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import Profile

"""
Açıklama:
Yeni bir kullanıcı oluştuğu zaman bu kullanıcıya ait OneToOne bağlantıda bir profil kaydı oluşturulması gerekmektedir.
Bunun için post_save signal kullanılmıştır.
"""


@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=None, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
