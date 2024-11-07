from django.db import models
from apps.common.models import BaseModel
from django.core.exceptions import ValidationError


class Comment(BaseModel):

    author = models.ForeignKey(
        "users.User", on_delete=models.DO_NOTHING, related_name="comments"
    )
    post = models.ForeignKey(
        "boards.Post", on_delete=models.DO_NOTHING, related_name="comments"
    )
    content = models.TextField()
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    is_deleted = models.BooleanField(default=False)

    def is_reply(self):
        return self.parent is not None

    def clean(self):
        """1 depth 대댓글만 허용하도록 검증"""
        if self.parent and self.parent.parent:
            raise ValidationError("Only 1 depth replies are allowed.")
