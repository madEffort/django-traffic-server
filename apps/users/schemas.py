from ninja import ModelSchema, Schema
from .models import User


class UserSchema(ModelSchema):

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class UserIn(Schema):
    username: str
    password: str
    first_name: str | None
    last_name: str | None


class UserOut(Schema):
    id: int
    username: str


class Error(Schema):
    detail: str
