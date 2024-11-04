from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

from .models import Board, Post
from .schemas import PostIn, PostOut
from apps.common.schemas import Error
from apps.users.models import User


@api_controller("/boards", tags=["boards"])
class BoardController:

    @route.post("/create")
    def create_board_handler(self):
        pass

    @route.post(
        "/{board_id}/posts/create",
        response={201: PostOut, 401: Error, 404: Error},
        auth=JWTAuth(),
    )
    def create_post_handler(self, request, board_id: int, data: PostIn):

        if not isinstance(request.user, User):
            return 401, {"detail": "Authentication credentials were not provided"}

        board: Board | None = Board.objects.filter(id=board_id).first()

        if not board:
            return 404, {"detail": "Board not found"}

        post: Post = Post.objects.create(
            title=data.title, content=data.content, author=request.user, board=board
        )

        return 201, post
