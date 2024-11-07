from urllib import request
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import PermissionDenied

from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth


from apps.comments.schemas import CommentIn, CommentOut
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

    @route.put(
        "/{board_id}/posts/{post_id}/comments/{comment_id}",
        response={200: CommentOut, 404: Error},
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
    )
    @transaction.atomic
    def delete_comment_handler(self, board_id: int, post_id: int, comment_id: int):
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
        response={200: list[CommentOut], 404: Error},
    )
    def get_comments_handler(self, board_id: int, post_id: int):
        """댓글 전체 조회"""

        _, post = self.get_board_and_post(board_id=board_id, post_id=post_id)

        comments = post.comments.all()

        return 200, comments

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

        comment = Comment.objects.create(
            author=request.user, post=post, content=data.content
        )

        return 201, comment
