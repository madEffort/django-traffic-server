from django.db import models

from apps.common.models import BaseModel


class Campaign(BaseModel):

    title = models.CharField(max_length=255)
    content = models.TextField()
    views = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)

    is_deleted = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)


class CampaignStatBase(BaseModel):
    campaign_id = models.BigIntegerField()
    count = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True


class CampaignViewStat(CampaignStatBase):
    pass


class CampaignClickStat(CampaignStatBase):
    pass
