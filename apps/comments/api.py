from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import PermissionDenied

from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth
from ninja_extra.pagination import (
    paginate,
    PageNumberPaginationExtra,
    PaginatedResponseSchema,
)

from apps.boards.tasks import send_notification
from apps.comments.schemas import CommentIn, CommentNotification, CommentOut
from apps.common.schemas import Error
from apps.boards.models import Board, Post

from .models import Comment


@api_controller("/boards", tags=["comments"])
class CommentController:

    def get_board_and_post(self, board_id: int, post_id: int):
        """게시판, 게시물 검증"""
        board = get_object_or_404(Board, id=board_id)
        post = Post.objects.filter(board=board, id=post_id, is_deleted=False).first()
        if not post:
            raise Http404("Post Not Found")

        return board, post

    """
    댓글 핸들러
    """

    @route.get(
        "/{board_id}/posts/{post_id}/comments/{comment_id}/replies",
        response=PaginatedResponseSchema[CommentOut],
    )
    @paginate(PageNumberPaginationExtra, page_size=20)
    def get_replies_handler(self, board_id: int, post_id: int, comment_id: int):
        """대댓글 조회 - 페이지네이션(20개)"""

        comment: Comment = get_object_or_404(
            Comment,
            id=comment_id,
            post_id=post_id,
            parent__isnull=True,
            is_deleted=False,
        )

        replies: list[Comment] = comment.replies.filter(
            is_deleted=False
        ).select_related("author")

        replies_data = [
            CommentOut(
                id=reply.id,
                parent=reply.parent.id if reply.parent else None,
                content=reply.content,
                author=reply.author,
                is_deleted=reply.is_deleted,
            )
            for reply in replies
        ]

        return replies_data

    @route.put(
        "/{board_id}/posts/{post_id}/comments/{comment_id}",
        response={200: CommentOut, 404: Error},
        auth=JWTAuth(),
    )
    @transaction.atomic
    def update_comment_handler(
        self, request, board_id: int, post_id: int, comment_id: int, data: CommentIn
    ):
        """댓글 수정"""

        _, post = self.get_board_and_post(board_id=board_id, post_id=post_id)

        comment: Comment | None = post.comments.filter(id=comment_id).first()

        if not comment:
            raise Http404("Comment Not Found")

        if not request.user == comment.author:
            raise PermissionDenied("Update Comment Forbidden")

        comment.content = data.content
        comment.save()

        return 200, comment

    @route.delete(
        "/{board_id}/posts/{post_id}/comments/{comment_id}",
        response={204: None, 404: Error},
        auth=JWTAuth(),
    )
    @transaction.atomic
    def delete_comment_handler(
        self, request, board_id: int, post_id: int, comment_id: int
    ):
        """댓글 삭제"""
        _, post = self.get_board_and_post(board_id=board_id, post_id=post_id)

        comment: Comment = post.comments.filter(id=comment_id).first()

        if not comment:
            raise Http404("Comment Not Found")

        if not (request.user == comment.author or request.user.is_staff):
            raise PermissionDenied("Delete Comment Forbidden")

        comment.delete()

        return 204, None

    @route.get(
        "/{board_id}/posts/{post_id}/comments",
        response=PaginatedResponseSchema[CommentOut],
    )
    @paginate(PageNumberPaginationExtra, page_size=20)
    def get_comments_handler(self, board_id: int, post_id: int):
        """루트 댓글 전체 조회 - 페이지네이션(20개)"""

        _, post = self.get_board_and_post(board_id=board_id, post_id=post_id)

        root_comments: list[Comment] = post.comments.filter(
            is_deleted=False, parent__isnull=True
        ).select_related("author")

        return root_comments

    @route.post(
        "/{board_id}/posts/{post_id}/comments",
        response={201: CommentOut, 404: Error},
        auth=JWTAuth(),
    )
    @transaction.atomic
    def create_comment_handler(
        self, request, board_id: int, post_id: int, data: CommentIn
    ):
        """댓글 생성"""

        _, post = self.get_board_and_post(board_id=board_id, post_id=post_id)

        if post.is_deleted:
            raise Http404("Post Not Found")

        parent_comment = None
        if data.parent:
            parent_comment: Comment | None = Comment.objects.filter(
                post=post, id=data.parent
            ).first()

            if not parent_comment:
                raise Http404("Parent Not Found")

        comment = Comment.objects.create(
            author=request.user, post=post, content=data.content, parent=parent_comment
        )

        # 댓글 작성 메시지 큐 추가
        comment_notification = CommentNotification(
            type="create_comment",
            user_id=request.user.id,
            comment_id=comment.id,
        )

        send_notification.delay(comment_notification.dict())

        return 201, comment
