from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

from .models import Board, Post
from .schemas import BoardIn, BoardOut, PostIn, PostOut
from apps.common.schemas import Error
from apps.users.models import User


@api_controller("/boards", tags=["boards"])
class BoardController:
    """
    게시판 핸들러
    """

    @route.post("/create", response={201: BoardOut, 404: Error})
    def create_board_handler(self, data: BoardIn):

        board, created = Board.objects.get_or_create(
            title=data.title, description=data.description
        )

        if not created:
            return 404, {"detail": "Board already exists"}

        return 201, board

    """
    게시글 핸들러
    """

    @route.post(
        "/{board_id}/posts/create",
        response={201: PostOut, 401: Error, 404: Error},
        auth=JWTAuth(),
    )
    def create_post_handler(self, request, board_id: int, data: PostIn):
        """게시판 생성"""

        if not isinstance(request.user, User):
            return 401, {"detail": "Authentication credentials were not provided"}

        board: Board | None = Board.objects.filter(id=board_id).first()

        if not board:
            return 404, {"detail": "Board not found"}

        post: Post = Post.objects.create(
            title=data.title, content=data.content, author=request.user, board=board
        )

        return 201, post

    @route.get("/{board_id}/posts", response={200: list[PostOut], 404: Error})
    def get_posts_handler(
        self, board_id: int, last_id: int = None, first_id: int = None
    ):
        """복수 게시글 조회"""

        board: Board | None = Board.objects.filter(id=board_id).first()

        if not board:
            return 404, {"detail": "Board not found"}

        posts_query = Post.objects.filter(board=board).order_by("-created_at")

        if last_id is not None:
            posts_query = posts_query.filter(id__lt=last_id)

        if first_id is not None:
            posts_query = posts_query.filter(id__gt=first_id)

        posts = posts_query[:10]

        return 200, posts
