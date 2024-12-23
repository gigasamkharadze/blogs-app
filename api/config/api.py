from ninja import NinjaAPI
from blogs.api.router import router as blog_router
from menu.api.router import router as menu_router
from tags.api.router import router as tags_router
from users.api.router import router as users_router

api = NinjaAPI(
    title='Blog API',
    description='Blog API with JWT authentication',
    version='1.0.0',
    docs_url='docs/',
    csrf=False,
)

# Register routers
api.add_router("/users/", users_router)
api.add_router("/blogs/", blog_router)
api.add_router("/menu/", menu_router)
api.add_router("/tags/", tags_router)
