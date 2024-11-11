from ninja import Schema


class Success(Schema):
    detail: str


class Error(Schema):
    detail: str
