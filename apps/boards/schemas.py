from ninja import ModelSchema, Schema
from .models import Post, Board
from apps.users.schemas import UserOut
from datetime import datetime


class BoardSchema(ModelSchema):

    class Meta:
        model = Board
        fields = ["id", "title", "description", "created_at", "updated_at"]


class BoardIn(Schema):
    title: str
    description: str


class BoardOut(Schema):
    id: int
    title: str
    description: str


class PostSchema(ModelSchema):

    class Meta:
        model = Post
        fields = [
            "id",
            "board",
            "author",
            "title",
            "content",
            "views",
            "is_deleted",
            "created_at",
            "updated_at",
        ]


class PostIn(Schema):
    title: str
    content: str


class PostUpdate(Schema):
    title: str | None = None
    content: str | None = None


class PostOut(Schema):
    id: int
    board: BoardOut
    author: UserOut
    title: str
    content: str
    views: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class PostNotification(Schema):
    type: str
    user_id: int
    post_id: int
