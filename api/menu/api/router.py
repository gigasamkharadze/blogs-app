from ninja import Router
from .schemas import MenuListSchema
from .endpoints import get_menu

router = Router(tags=["Menu"])

router.add_api_operation(
    "/",
    ["GET"],
    get_menu,
    response=MenuListSchema,
    summary="Get menu structure",
    description="Get the complete menu structure with nested items"
)