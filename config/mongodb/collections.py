# from .client import db

# campaign_view_collection = db["campaign_view_history"]
# campaign_click_collection = db["campaign_click_history"]
# user_notification_collection = db["user_notification_history"]

from pymongo.collection import Collection
from .client import db


class BaseCollection:
    def __init__(self, collection: Collection):
        self.collection = collection

    def insert_one(self, data, session=None):
        """데이터 삽입"""
        return self.collection.insert_one(data)

    def find_one(self, filter, session=None):
        """조건에 맞는 단일 문서 조회"""
        return self.collection.find_one(filter)

    def find_many(self, filter, session=None):
        """조건에 맞는 여러 문서 조회"""
        return self.collection.find(filter)

    def update_one(self, filter, updated_data, session=None):
        """단일 문서 업데이트"""
        return self.collection.update_one(filter, {"$set": updated_data})

    def delete_one(self, filter, session=None):
        """단일 문서 삭제"""
        return self.collection.delete_one(filter)

    def aggregate(self, pipeline, session=None):
        """Aggregation 파이프라인 실행"""
        return self.collection.aggregate(pipeline)


class CampaignViewCollection(BaseCollection):
    def __init__(self):
        super().__init__(db["campaign_view_history"])


class CampaignClickCollection(BaseCollection):
    def __init__(self):
        super().__init__(db["campaign_click_history"])


class UserNotificationCollection(BaseCollection):
    def __init__(self):
        super().__init__(db["user_notification_history"])

    def mark_as_read(self, notification_id, session=None):
        """알림을 읽음 상태로 변경"""
        return self.update_one({"_id": notification_id}, {"is_read": True})
