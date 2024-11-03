from django.contrib.auth.hashers import check_password
from ninja_extra import api_controller, route
from .models import User
from .schemas import Error, UserSchema, UserIn, UserOut


@api_controller("/users", tags=["users"], permissions=[])
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

    @route.delete("/{user_id}", response={204: None, 404: Error})
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
