from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth
import json

from apps.common.schemas import Error
from apps.users.models import User
from .schemas import Device


@api_controller("/devices", tags=["devices"])
class DeviceController:

    @route.get("", response={200: list[Device], 404: Error}, auth=JWTAuth())
    def get_own_devices_handler(self, request):
        """본인의 디바이스 전체 조회"""
        user: User | None = User.objects.filter(id=request.user.id).first()
        if not user:
            return 404, {"detail": "User Not Found"}

        devices: list[Device] = [json.loads(device) for device in user.devices]

        return 200, devices

    @route.post("", response={200: Device, 400: Error, 404: Error}, auth=JWTAuth())
    def add_device_handler(self, request, data: Device):
        """디바이스 추가"""
        user: User | None = User.objects.filter(id=request.user.id).first()
        if not user:
            return 404, {"detail": "User Not Found"}

        device_json = json.dumps(data.dict())

        if device_json in user.devices:
            return 400, {"detail", "Bad Request"}  # 이미 등록된 디바이스

        user.devices.append(device_json)
        user.save()

        return 200, Device(name=data.name, token=data.token)
