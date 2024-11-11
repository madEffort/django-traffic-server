from mongoengine import connect
from . import settings


def initialize_mongo_connection():
    connect(
        db=settings.MONGO_DB_NAME,
        host=settings.MONGO_URI,
    )
