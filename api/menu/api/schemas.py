from ninja import Schema
from typing import List


class MenuSchema(Schema):
    id: int
    title: str
    url: str
    order: int


class MenuListSchema(Schema):
    items: List[MenuSchema]
