from datetime import datetime
from mongoengine import Document, StringField, BooleanField, DateTimeField, LongField


class CampaignViewHistory(Document):
    campaign_id = LongField()
    user_id = LongField()
    client_ip = StringField()
    is_true_view = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)

    meta = {"collection": "campaign_view_history"}


class CampaignClickHistory(Document):
    campaign_id = LongField()
    user_id = LongField()
    client_ip = StringField()
    created_at = DateTimeField(default=datetime.now)

    meta = {"collection": "campaign_click_history"}
