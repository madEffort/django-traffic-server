from django.db import models
from apps.common.models import BaseModel


class Comment(BaseModel):

    author = models.ForeignKey(
        "users.User", on_delete=models.DO_NOTHING, related_name="comments"
    )
    post = models.ForeignKey(
        "boards.Post", on_delete=models.DO_NOTHING, related_name="comments"
    )
    content = models.TextField()
    is_deleted = models.BooleanField(default=False)
