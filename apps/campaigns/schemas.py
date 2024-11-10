from datetime import datetime
from ninja import ModelSchema, Schema

from .models import Campaign


class CampaignSchema(ModelSchema):

    class Meta:
        model = Campaign
        fields = [
            "id",
            "title",
            "content",
            "views",
            "clicks",
            "start_date",
            "end_date",
            "is_deleted",
            "is_visible",
        ]


class CampaignIn(Schema):
    title: str
    content: str


class CampaignOut(Schema):
    id: int
    title: str
    content: str
    views: int
    clicks: int
    start_date: datetime
    end_date: datetime
    is_deleted: bool
    is_visible: bool
