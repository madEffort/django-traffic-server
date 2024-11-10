from ninja_extra import api_controller, route

from apps.common.schemas import Error

from .models import Campaign
from .schemas import CampaignIn, CampaignOut


@api_controller("/campaigns", tags=["campaigns"])
class CampaignController:

    @route.get("/{campaign_id}", response={200: CampaignOut, 404: Error})
    def get_campaign_handler(self, campaign_id: int):
        """캠페인(광고) 단일 조회"""

        campaign = Campaign.objects.filter(id=campaign_id).first()
        if not campaign:
            return 404, {"detail": "Campaign Not Found"}

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
            title=data.title, content=data.content
        )

        if not created:
            return 400, {"detail": "Bad Request"}

        return 201, campaign
