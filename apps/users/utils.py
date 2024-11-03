from django.conf import settings
from django.http import HttpRequest


def get_refresh_token(request: HttpRequest) -> str | None:
    """쿠키 또는 Authorization 헤더에서 refresh_token을 가져오는 유틸리티 함수"""
    refresh_token = request.COOKIES.get(settings.NINJA_JWT["AUTH_COOKIE_REFRESH"])

    # 쿠키에 없을 경우 Authorization 헤더에서 Bearer 토큰을 가져옴
    if not refresh_token:
        refresh_token = (
            request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
            if request.headers.get("Authorization", "").startswith("Bearer ")
            else None
        )

    return refresh_token
