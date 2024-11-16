from ninja import Schema


class Device(Schema):
    name: str
    token: str
