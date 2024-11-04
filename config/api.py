from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from apps.users.api import UserController
from apps.boards.api import BoardController

api = NinjaExtraAPI(title="Django Ninja Boilerplate API")


api.register_controllers(
    NinjaJWTDefaultController,
    UserController,
    BoardController,
)
