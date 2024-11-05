from ninja import ModelSchema, Schema

from apps.users.schemas import UserOut

from .models import Comment


class CommentSchema(ModelSchema):

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "post",
            "content",
            "is_deleted",
            "created_at",
            "updated_at",
        ]


class CommentIn(Schema):
    content: str


class CommentOut(Schema):
    id: int
    author: UserOut
    content: str
