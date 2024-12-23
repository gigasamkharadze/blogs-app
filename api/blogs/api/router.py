from ninja import Router
from config.auth import AuthBearer

from .schemas import (
    BlogDetailSchema,
    PaginatedBlogsSchema,
    ErrorSchema,
    CommentSchema,
    CommentListSchema,
    CategorySchema,
    CategoryListSchema
)
from .endpoints import (
    list_blogs,
    get_blog,
    create_blog,
    update_blog,
    delete_blog,
    list_blog_comments,
    create_comment,
    update_comment,
    delete_comment,
    like_comment,
    dislike_comment,
    list_categories,
    get_category
)

router = Router(tags=["Blogs"])


router.add_api_operation(
    "/categories",
    ["GET"],
    list_categories,
    response=CategoryListSchema,
    summary="List all categories"
)

router.add_api_operation(
    "/categories/{category_id}",
    ["GET"],
    get_category,
    response=CategorySchema,
    summary="Get a category"
)

router.add_api_operation(
    "/",
    ["GET"],
    list_blogs,
    response=PaginatedBlogsSchema,
    summary="List all blogs"
)

router.add_api_operation(
    "/{blog_id}",
    ["GET"],
    get_blog,
    response=BlogDetailSchema,
    summary="Get a blog"
)

router.add_api_operation(
    "/",
    ["POST"],
    create_blog,
    response={201: BlogDetailSchema, 400: ErrorSchema},
    auth=AuthBearer(),
    summary="Create a blog"
)

router.add_api_operation(
    "/{blog_id}",
    ["PUT"],
    update_blog,
    response={
        200: BlogDetailSchema,
        400: ErrorSchema,
        401: ErrorSchema,
        403: ErrorSchema
    },
    auth=AuthBearer(),
    summary="Update a blog"
)

router.add_api_operation(
    "/{blog_id}",
    ["DELETE"],
    delete_blog,
    response={204: None, 403: ErrorSchema, 404: ErrorSchema},
    auth=AuthBearer(),
    summary="Delete a blog"
)

# Comment routes
router.add_api_operation(
    "/{blog_id}/comments/",
    ["GET"],
    list_blog_comments,
    response=CommentListSchema,
    summary="List blog comments"
)

router.add_api_operation(
    "/{blog_id}/comments/",
    ["POST"],
    create_comment,
    response={201: CommentSchema, 400: ErrorSchema},
    auth=AuthBearer(),
    summary="Create a comment"
)

router.add_api_operation(
    "/{blog_id}/comments/{comment_id}/",
    ["PUT"],
    update_comment,
    response={200: CommentSchema, 400: ErrorSchema, 403: ErrorSchema},
    auth=AuthBearer(),
    summary="Update a comment"
)

router.add_api_operation(
    "/{blog_id}/comments/{comment_id}/",
    ["DELETE"],
    delete_comment,
    response={204: None, 403: ErrorSchema, 404: ErrorSchema},
    auth=AuthBearer(),
    summary="Delete a comment"
)

# Comment like/dislike routes
router.add_api_operation(
    "/{blog_id}/comments/{comment_id}/like/",
    ["POST"],
    like_comment,
    response={200: CommentSchema, 400: ErrorSchema, 403: ErrorSchema},
    auth=AuthBearer(),
    summary="Like a comment"
)

router.add_api_operation(
    "/{blog_id}/comments/{comment_id}/dislike/",
    ["POST"],
    dislike_comment,
    response={200: CommentSchema, 400: ErrorSchema, 403: ErrorSchema},
    auth=AuthBearer(),
    summary="Dislike a comment"
)