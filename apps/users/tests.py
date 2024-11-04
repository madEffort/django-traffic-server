from django.test import TestCase
from ninja.testing import TestClient
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

    def test_get_users(self):
        """유저 전체 조회"""
        response = self.client.get("/api/users/")

        # 예상 데이터
        expected_data = [
            UserSchema.from_orm(self.user1).dict(),
            UserSchema.from_orm(self.user2).dict(),
        ]

        assert response.status_code == 200
        assert response.json() == expected_data
