from mongoengine import connect
from . import settings


# 이미 연결된 MongoDB 클라이언트를 저장할 변수
_mongo_client = None


def get_mongo_client():
    global _mongo_client
    if _mongo_client is None:
        # 최초 호출 시에만 MongoDB에 연결 설정
        _mongo_client = connect(
            db=settings.MONGO_DB_NAME,
            host=settings.MONGO_HOST,
            port=settings.MONGO_PORT,
            username=settings.MONGO_USER,
            password=settings.MONGO_PASSWORD,
        )
    return _mongo_client
