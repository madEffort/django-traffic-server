from ninja import ModelSchema, Schema

from apps.users.schemas import UserOut

from .models import Comment


class CommentSchema(ModelSchema):

    class Meta:
        model = Comment
        fields = [
            "id",
            "parent",
            "author",
            "post",
            "content",
            "is_deleted",
            "created_at",
            "updated_at",
        ]


class CommentIn(Schema):
    parent: int | None = None
    content: str


class CommentOut(Schema):
    id: int
    parent: int | None = None
    content: str
    author: UserOut
    is_deleted: bool

    class Config:
        orm_mode = True
