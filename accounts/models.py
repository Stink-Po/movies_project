from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField()

