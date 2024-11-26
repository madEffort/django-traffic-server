from pymongo import MongoClient
from threading import Lock
from .settings import MONGO_URI, MONGO_DB_NAME


class MongoDBClient:
    _instance = None
    _lock = Lock()  # 멀티스레드 환경에서의 안전성을 위한 락

    def __new__(cls, *args, **kwargs):
        if not cls._instance:  # 기존 인스턴스가 없을 때만 락을 사용해 초기화
            with cls._lock:
                if not cls._instance:  # 다시 확인 (Double-Checked Locking)
                    cls._instance = super().__new__(cls, *args, **kwargs)
                    cls._instance._client = MongoClient(MONGO_URI)
                    cls._instance._db = cls._instance._client[MONGO_DB_NAME]
        return cls._instance

    @property
    def db(self):
        """데이터베이스 객체에 접근"""
        return self._db


mongo_client = MongoDBClient()
db = mongo_client.db
