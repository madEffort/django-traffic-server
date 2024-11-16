from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField


class User(AbstractUser):

    username = models.EmailField(unique=True)
    devices = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        default=list,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.username
