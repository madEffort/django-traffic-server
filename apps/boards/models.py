from django.db import models
from apps.common.models import BaseModel


class Board(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=False, null=False)


class Post(BaseModel):
    board = models.ForeignKey(
        "boards.Board", on_delete=models.DO_NOTHING, related_name="posts"
    )
    author = models.ForeignKey(
        "users.User", on_delete=models.DO_NOTHING, related_name="posts"
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=False, null=False)
    views = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
