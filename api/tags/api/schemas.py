from ninja import Schema

class TagSchema(Schema):
    id: int
    name: str
    count: int
