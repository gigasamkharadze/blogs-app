from ninja import Schema
from typing import List, Optional
from datetime import datetime


class ErrorSchema(Schema):
    message: str


class BlogListSchema(Schema):
    id: int
    title: str
    image: Optional[str]
    author: str
    category: Optional[str]
    tags: List[str]
    created_at: datetime
    is_active: bool


class BlogDetailSchema(BlogListSchema):
    content: str


class BlogCreateSchema(Schema):
    title: str
    content: str
    category_id: Optional[int] = None
    tags: List[str] = []
    is_active: bool = True


class BlogUpdateSchema(Schema):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class PaginatedBlogsSchema(Schema):
    count: int
    next: Optional[int]
    previous: Optional[int]
    results: List[BlogListSchema]


class BlogFilterSchema(Schema):
    page: int = 1
    page_size: int = 10
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    author_id: Optional[int] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    search: Optional[str] = None


class CommentCreateSchema(Schema):
    content: str
    parent_id: Optional[int] = None


class CommentUpdateSchema(Schema):
    content: str


class CommentSchema(Schema):
    id: int
    content: str
    author: str
    blog_id: int
    parent_id: Optional[int] = None
    created_at: datetime
    likes: int = 0
    dislikes: int = 0
    children: List['CommentSchema'] = []


class CommentListSchema(Schema):
    count: int
    results: List[CommentSchema]


class TagSchema(Schema):
    id: int
    name: str
    slug: str
    count: int


class CategorySchema(Schema):
    id: int
    title: str
    parent_id: Optional[int] = None
    children: List['CategorySchema'] = []


class CategoryListSchema(Schema):
    count: int
    results: List[CategorySchema]
