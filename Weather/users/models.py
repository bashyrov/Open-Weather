from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    users_city = models.CharField('City Name', max_length=50, default="")
    tg_username = models.CharField('Telegram Username', max_length=50, default="")
    del_time = models.TimeField('Deletion Time', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.users_city = str(self.users_city).title()
        super(User, self).save(*args, **kwargs)


