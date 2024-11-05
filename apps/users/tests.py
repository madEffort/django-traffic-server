from django.test import TestCase
from ninja.testing import TestClient
from ninja_jwt.tokens import RefreshToken
from config.api import api

from apps.users.models import User
from apps.users.schemas import UserSchema


class UserControllerTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = TestClient(api)

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1@example.com", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="user2@example.com", password="password123"
        )
        self.token = RefreshToken.for_user(self.user1)

    def test_create_user_handler(self):
        """유저 생성 테스트"""
        pass

    def test_login_user_handler(self):
        """유저 로그인 테스트"""

        response = self.client.post(
            "/api/users/login",
            data={
                "username": "user1@example.com",
                "password": "password123",
                "first_name": "user1",
                "last_name": "user1",
            },
            content_type="application/json",
        )

        assert response.status_code == 200
        assert "access" in response.json()
        assert "refresh" in response.json()

    def test_logout_user_handler(self):
        """유저 로그아웃 테스트"""
        pass

    def test_delete_user_handler(self):
        """유저 삭제 테스트"""
        pass

    def test_get_users_handler(self):
        """유저 전체 조회 테스트"""

        response = self.client.get("/api/users")

        # 예상 데이터
        expected_data = [
            UserSchema.from_orm(self.user1).dict(),
            UserSchema.from_orm(self.user2).dict(),
        ]

        assert response.status_code == 200
        assert response.json() == expected_data

    def test_get_user_handler(self):
        """유저 단일 조회 테스트"""

        response = self.client.get(
            "/api/users/1",
            headers={"Authorization": f"Bearer {str(self.token.access_token)}"},
        )

        expected_data = UserSchema.from_orm(self.user1).dict()

        assert response.status_code == 200
        assert response.json() == expected_data
