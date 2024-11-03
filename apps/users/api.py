from django.contrib.auth import authenticate
from django.middleware import csrf
from django.http import JsonResponse, HttpResponse
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken
from ninja.responses import Response

from config import settings
from .models import User
from .schemas import Error, UserSchema, UserIn, UserOut, JWTToken


@api_controller("/users", tags=["users"])
class UserController:

    @route.post("/create", response={201: UserOut, 400: Error})
    def post_user_handler(self, data: UserIn):
        """유저 생성"""
        if User.objects.filter(username=data.username).exists():
            return 400, {"detail": "Username already exists."}

        user: User = User(username=data.username)
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.set_password(data.password)
        user.save()

        return 201, user

    @route.post("/login", response={200: JWTToken, 401: Error})
    def login_user_handler(self, request, data: UserIn):
        """유저 로그인"""

        user = authenticate(username=data.username, password=data.password)

        if not user:
            return 401, {"detail": "Invalid username or password"}

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response_data = {"access": access_token, "refresh": refresh_token}

        response = JsonResponse(response_data, status=200)
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

        return response

    @route.post("/logout", response={200: None, 400: Error}, auth=JWTAuth())
    def logout_user_handler(self, request):
        """유저 로그아웃"""

        refresh_token = (
            request.COOKIES.get(settings.NINJA_JWT["AUTH_COOKIE_REFRESH"])
        ) or (request.headers.get("Authorization").split(" ")[1])

        if not refresh_token:
            return 400, {"detail": "Failed to logout"}

        token = RefreshToken(refresh_token)
        token.blacklist()

        response = HttpResponse()
        response.delete_cookie(settings.NINJA_JWT["AUTH_COOKIE"])
        response.delete_cookie(settings.NINJA_JWT["AUTH_COOKIE_REFRESH"])
        response.delete_cookie("X-CSRFToken")
        response.delete_cookie("csrftoken")
        response["X-CSRFToken"] = None

        return 200, response

    @route.delete("/{user_id}", response={204: None, 404: Error}, auth=JWTAuth())
    def delete_user_handler(self, user_id):
        """유저 삭제"""
        user: User | None = User.objects.filter(id=user_id).first()
        if not user:
            return 404, {"detail": "User not found"}

        user.delete()
        return 204, None

    @route.get("/", response={200: list[UserSchema]})
    def get_users_handler(self):
        """유저 전체 조회"""
        users: list[User] = User.objects.all()

        return 200, users

    @route.get("/{user_id}", response={200: UserSchema, 404: Error})
    def get_user_handler(self, user_id: int):
        """유저 단일 조회"""
        user: User | None = User.objects.filter(id=user_id).first()

        if not user:
            return 404, {"detail": "Not Found"}

        return 200, user
