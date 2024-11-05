from ninja_extra import api_controller, route, throttle
from ninja_jwt.authentication import JWTAuth

from .models import Board, Post
from .schemas import BoardIn, BoardOut, PostIn, PostOut, PostUpdate
from apps.common.schemas import Error


@api_controller("/boards", tags=["boards"])
class BoardController:
    """
    게시판 핸들러
    """

    @route.post("/create", response={201: BoardOut, 400: Error})
    def create_board_handler(self, data: BoardIn):

        board, created = Board.objects.get_or_create(
            title=data.title, description=data.description
        )

        if not created:
            return 400, {"detail": "Bad Request"}

        return 201, board

    """
    게시글 핸들러
    """

    @route.post(
        "/{board_id}/posts/create",
        response={201: PostOut, 404: Error},
        auth=JWTAuth(),
    )
    @throttle
    def create_post_handler(self, request, board_id: int, data: PostIn):
        """게시글 생성"""

        board: Board | None = Board.objects.filter(id=board_id).first()
        if not board:
            return 404, {"detail": "Board Not Found"}

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
            return 404, {"detail": "Board Not Found"}

        posts_query = Post.objects.filter(board=board, is_deleted=False).order_by(
            "-created_at"
        )

        if last_id is not None:
            posts_query = posts_query.filter(id__lt=last_id)

        if first_id is not None:
            posts_query = posts_query.filter(id__gt=first_id)

        posts = posts_query[:10]

        return 200, posts

    @route.put(
        "/{board_id}/posts/{post_id}",
        response={200: PostOut, 403: Error, 404: Error},
        auth=JWTAuth(),
    )
    def update_post_handler(
        self, request, board_id: int, post_id: int, data: PostUpdate
    ):
        """게시글 수정"""

        board: Board | None = Board.objects.filter(id=board_id).first()
        if not board:
            return 404, {"detail": "Board Not Found"}

        post: Post | None = Post.objects.filter(
            board=board, id=post_id, is_deleted=False
        ).first()
        if not post:
            return 404, {"detail": "Post Not Found"}

        if not (request.user == post.author or request.user.is_staff):
            return 403, {"detail": "Update Post Forbidden"}

        # 부분 업데이트
        for field, value in data.dict(exclude_unset=True).items():
            setattr(post, field, value)
        post.save()

        return 200, post

    @route.delete(
        "/{board_id}/posts/{post_id}",
        response={200: PostOut, 403: Error, 404: Error},
        auth=JWTAuth(),
    )
    def delete_post_handler(self, request, board_id: int, post_id: int):
        """게시글 삭제"""

        board: Board | None = Board.objects.filter(id=board_id).first()
        if not board:
            return 404, {"detail": "Board Not Found"}

        post: Post | None = Post.objects.filter(
            board=board, id=post_id, is_deleted=False
        ).first()
        if not post:
            return 404, {"detail": "Post Not Found"}

        if not (request.user == post.author or request.user.is_staff):
            return 403, {"detail": "Delete Post Forbidden"}

        post.is_deleted = True
        post.save()

        return 200, post
