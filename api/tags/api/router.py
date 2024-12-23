from ninja import Router
from typing import List
from .schemas import TagSchema
from .endpoints import list_tags

router = Router(tags=["Tags"])

router.add_api_operation(
    "/",
    ["GET"],
    list_tags,
    response=List[TagSchema],
    summary="List all tags",
    description="Get all available tags with their usage count"
)