from celery import shared_task

from apps.boards.models import Post
from apps.comments.models import Comment
from apps.comments.schemas import CommentNotification


@shared_task(queue="send_notification_queue")
def send_notification(message):
    """메세지 전송"""

    if "type" in message:

        # 댓글 작성 메시지일 경우
        if message["type"] == "create_comment":

            comment_id = int(message["comment_id"])
            user_id = int(message["user_id"])

            # 댓글 작성자가 작성한 게시물 가져오기
            post: Post = (
                Comment.objects.filter(id=comment_id)
                .select_related("post__author")
                .first()
                .post
            )

            # 게시글 작성자 및 댓글 작성자 ID 가져오기
            user_ids = post.comments.values_list(
                "author_id", flat=True
            ).distinct()  # 댓글 작성자 ID  # 중복 제거

            # 유니크한 사용자 ID 세트
            notified_users = set(user_ids)
            notified_users.add(post.author.id)  # 게시글 작성자 추가
            notified_users.add(user_id)  # 댓글 작성자 본인은 제외

            # 알림 발송
            for notified_user_id in notified_users:
                send_notification.delay(
                    CommentNotification(
                        type="send_notification",
                        user_id=notified_user_id,
                        comment_id=comment_id,
                    ).dict()
                )

    return f"메시지 전송: {message}"
