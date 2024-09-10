from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    birthday = models.DateField()
    gender = models.CharField(max_length=10, blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username