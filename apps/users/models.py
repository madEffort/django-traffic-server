from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    username = models.EmailField(unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.username
