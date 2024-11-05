from django.contrib.auth import authenticate
from django.middleware import csrf
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken
from ninja.responses import Response

from django.conf import settings
from apps.common.schemas import Error
from .models import User
from .schemas import UserIn, UserOut, JWTToken
from .utils import get_refresh_token


@api_controller("/users", tags=["users"])
class UserController:

    @route.post("/create", response={201: UserOut, 400: Error})
    def create_user_handler(self, data: UserIn):
        """유저 생성"""

        user, created = User.objects.get_or_create(
            username=data.username,
            defaults={
                "first_name": data.first_name,
                "last_name": data.last_name,
            },
        )

        if not created:
            return 400, {"detail": "Bad Request"}

        user.set_password(data.password)
        user.save()

        return 201, user

    @route.post("/login", response={200: JWTToken, 404: Error})
    def login_user_handler(self, request, data: UserIn):
        """유저 로그인"""

        user: User | None = authenticate(username=data.username, password=data.password)
        if not user:
            return 404, {"detail": "User Not Found"}

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response_data = {"access": access_token, "refresh": refresh_token}

        response = Response(response_data, status=200)
        response.set_cookie(
            key=settings.NINJA_JWT["AUTH_COOKIE"],
            value=access_token,
            expires=settings.NINJA_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=settings.NINJA_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.NINJA_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.NINJA_JWT["AUTH_COOKIE_SAMESITE"],
        )

        response.set_cookie(
            key=settings.NINJA_JWT["AUTH_COOKIE_REFRESH"],
            value=refresh_token,
            expires=settings.NINJA_JWT["REFRESH_TOKEN_LIFETIME"],
            secure=settings.NINJA_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.NINJA_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.NINJA_JWT["AUTH_COOKIE_SAMESITE"],
        )

        # CSRF 토큰 설정
        response["X-CSRFToken"] = csrf.get_token(request)

        return response  # 200

    @route.post("/logout", response={200: None, 400: Error}, auth=JWTAuth())
    def logout_user_handler(self, request):
        """유저 로그아웃"""

        refresh_token: str | None = get_refresh_token(request=request)

        if not refresh_token:
            return 400, {"detail": "Bad Request"}

        token = RefreshToken(refresh_token)
        token.blacklist()

        response = Response({"detail": "Logout OK"}, status=200)
        response.delete_cookie(settings.NINJA_JWT["AUTH_COOKIE"])
        response.delete_cookie(settings.NINJA_JWT["AUTH_COOKIE_REFRESH"])
        response.delete_cookie("X-CSRFToken")
        response.delete_cookie("csrftoken")
        response["X-CSRFToken"] = None

        return response  # 200

    @route.delete(
        "/{user_id}", response={204: None, 403: Error, 404: Error}, auth=JWTAuth()
    )
    def delete_user_handler(self, request, user_id: int):
        """유저 삭제"""

        user: User | None = User.objects.filter(id=user_id).first()
        if not user:
            return 404, {"detail": "User Not Found"}

        if not (request.user == user or request.user.is_staff):
            return 403, {"detail": "Delete User Forbidden"}

        user.delete()
        return 204, None

    @route.get("", response={200: list[UserOut]})
    def get_users_handler(self):
        """유저 전체 조회"""

        users: list[User] = User.objects.all()

        return 200, users

    @route.get("/{user_id}", response={200: UserOut, 404: Error})
    def get_user_handler(self, user_id: int):
        """유저 단일 조회"""

        user: User | None = User.objects.filter(id=user_id).first()
        if not user:
            return 404, {"detail": "User Not Found"}

        return 200, user
