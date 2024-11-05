from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth


from apps.comments.schemas import CommentOut
from apps.common.schemas import Error
from apps.boards.models import Board, Post


@api_controller("/boards", tags=["comments"])
class CommentController:

    def get_board_and_post(self, board_id: int, post_id: int):
        board = Board.objects.filter(id=board_id).first()
        if not board:
            return None, None

        post = Post.objects.filter(board=board, id=post_id, is_deleted=False).first()
        if not post:
            return board, None

        return board, post

    @route.get(
        "/{board_id}/posts/{post_id}/comments",
        response={200: list[CommentOut], 404: Error},
    )
    def get_comments_handler(self, board_id: int, post_id: int):

        board, post = self.get_board_and_post(board_id=board_id, post_id=post_id)
        if not board:
            return 404, {"detail": "Board Not Found"}
        if not post:
            return 404, {"detail": "Post Not Found"}

        comments = post.comments.all()

        return 200, comments
