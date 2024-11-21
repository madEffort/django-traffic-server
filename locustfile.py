from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    # 요청 간 대기 시간: 1초 ~ 5초
    host = "http://app:8000"
    wait_time = between(1, 5)

    @task  # 1000 / 100 기준 330 RPS
    def get_users(self):
        self.client.get("/api/users")
