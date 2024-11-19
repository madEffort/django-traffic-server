from celery import shared_task


@shared_task(queue="send_notification_queue")
def send_notification(message):
    """메세지 전송"""
    import logging

    logging.warn(f"전송받은 메시지: {message}")
    return f"메시지 전송: {message}"
