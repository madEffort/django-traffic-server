from celery import shared_task


@shared_task(queue="send_notification_queue")
def send_notification(message):
    """메세지 전송"""
    print(f"전송된 메시지: {message}")
    return f"메시지 전송: {message}"
