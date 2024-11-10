from django.core.cache import cache
from django.shortcuts import get_object_or_404
from ninja_extra import api_controller, route

from apps.common.schemas import Error

from .models import Campaign
from .schemas import CampaignIn, CampaignOut


@api_controller("/campaigns", tags=["campaigns"])
class CampaignController:

    def get_campaign_cache_key(self, campaign_id: int) -> str:
        return f"campaign:{campaign_id}"

    @route.get("/{campaign_id}", response={200: CampaignOut, 404: Error})
    def get_campaign_handler(self, campaign_id: int):
        """캠페인(광고) 단일 조회"""

        cache_key = self.get_campaign_cache_key(campaign_id=campaign_id)

        campaign: Campaign | None = cache.get(cache_key)
        if not campaign:
            campaign = get_object_or_404(Campaign, id=campaign_id)

            cache.set(cache_key, campaign, timeout=300)

        return 200, campaign

    @route.get("", response={200: list[CampaignOut], 404: Error})
    def get_campaigns_handler(self):
        """캠페인(광고) 전체 조회"""

        campaigns: list[Campaign] = Campaign.objects.all()

        return 200, campaigns

    @route.post("", response={201: CampaignOut, 400: Error, 404: Error})
    def create_campaign_handler(self, data: CampaignIn):
        """캠페인(광고) 생성"""

        campaign, created = Campaign.objects.get_or_create(
            title=data.title,
            content=data.content,
            start_date=data.start_date,
            end_date=data.end_date,
        )

        if not created:
            return 400, {"detail": "Bad Request"}

        cache_key = self.get_campaign_cache_key(campaign_id=campaign.id)
        cache.set(cache_key, campaign, timeout=300)

        return 201, campaign