from ninja import File, Form, Query
from ninja.files import UploadedFile
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from blogs.models import Blog, Comment, Category
from .schemas import (
    BlogCreateSchema,
    BlogFilterSchema,
    CommentCreateSchema,
    CommentUpdateSchema,
)
from datetime import datetime, timedelta
from typing import Optional
from django.utils import timezone

import json


def list_blogs(request, filters: BlogFilterSchema = Query(...)):
    queryset = Blog.objects.filter(is_active=True).order_by('-created_at')

    if filters.date_from or filters.date_to:
        try:
            if filters.date_from:
                from_date = datetime.strptime(filters.date_from, '%Y-%m-%d')
                from_date = timezone.make_aware(
                    datetime.combine(from_date.date(), datetime.min.time())
                )
                queryset = queryset.filter(created_at__gte=from_date)

            if filters.date_to:
                to_date = datetime.strptime(filters.date_to, '%Y-%m-%d')
                to_date = timezone.make_aware(
                    datetime.combine(to_date.date(), datetime.max.time())
                )
                queryset = queryset.filter(created_at__lte=to_date)

        except ValueError:
            pass

    if filters.author_id:
        queryset = queryset.filter(author_id=filters.author_id)

    if filters.category_id:
        queryset = queryset.filter(category_id=filters.category_id)

    if filters.tags:
        queryset = queryset.filter(tags__name__in=filters.tags).distinct()

    if filters.search:
        queryset = queryset.filter(
            Q(title__icontains=filters.search) |
            Q(content__icontains=filters.search)
        )

    paginator = Paginator(queryset, filters.page_size)
    page_obj = paginator.get_page(filters.page)

    return {
        "count": paginator.count,
        "next": page_obj.next_page_number() if page_obj.has_next() else None,
        "previous": page_obj.previous_page_number() if page_obj.has_previous() else None,
        "results": [
            {
                "id": blog.id,
                "title": blog.title,
                "image": blog.image.url if blog.image else None,
                "author": blog.author.username,
                "category": blog.category.title if blog.category else None,
                "tags": [tag.name for tag in blog.tags.all()],
                "created_at": blog.created_at,
                "is_active": blog.is_active,
                "content": blog.content
            }
            for blog in page_obj.object_list
        ]
    }


def get_blog(request, blog_id: int):
    blog = get_object_or_404(Blog, id=blog_id, is_active=True)
    return {
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "image": blog.image.url if blog.image else None,
        "author": blog.author.username,
        "category": blog.category.title if blog.category else None,
        "tags": [tag.name for tag in blog.tags.all()],
        "created_at": blog.created_at,
        "is_active": blog.is_active
    }


def create_blog(request, blog: BlogCreateSchema, image: UploadedFile = File(None)):
    try:
        new_blog = Blog.objects.create(
            title=blog.title,
            content=blog.content,
            author=request.auth,
            category_id=blog.category_id,
            is_active=blog.is_active
        )

        if image:
            new_blog.image.save(image.name, image)

        new_blog.tags.add(*blog.tags)

        return 201, {
            "id": new_blog.id,
            "title": new_blog.title,
            "content": new_blog.content,
            "image": new_blog.image.url if new_blog.image else None,
            "author": new_blog.author.username,
            "category": new_blog.category.title if new_blog.category else None,
            "tags": [tag.name for tag in new_blog.tags.all()],
            "created_at": new_blog.created_at,
            "is_active": new_blog.is_active
        }
    except Exception as e:
        return 400, {"message": str(e)}


def update_blog(
        request,
        blog_id: int,
        title: Optional[str] = Form(None),
        content: Optional[str] = Form(None),
        category_id: Optional[int] = Form(None),
        tags: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(None),
        image: Optional[UploadedFile] = File(None)
):
    if not request.auth:
        return 401, {"message": "Authentication required"}

    try:
        print("Received update data:")
        print(f"title: {title}")
        print(f"content: {content}")
        print(f"category_id: {category_id}")
        print(f"tags: {tags}")
        print(f"is_active: {is_active}")
        print(f"image: {image}")

        existing_blog = get_object_or_404(Blog, id=blog_id)

        if existing_blog.author != request.auth:
            return 403, {"message": "You can only edit your own blogs"}

        if title is not None:
            existing_blog.title = title
            print(f"Updated title to: {existing_blog.title}")

        if content is not None:
            existing_blog.content = content
            print(f"Updated content to: {existing_blog.content}")

        if category_id is not None:
            try:
                if isinstance(category_id, str) and category_id.strip():
                    category_id = int(category_id)
                existing_blog.category_id = category_id
                print(f"Updated category_id to: {existing_blog.category_id}")
            except (ValueError, TypeError):
                existing_blog.category_id = None
                print("Set category_id to None due to invalid value")

        if is_active is not None:
            if isinstance(is_active, str):
                is_active = is_active.lower() == 'true'
            existing_blog.is_active = is_active
            print(f"Updated is_active to: {existing_blog.is_active}")

        if image:
            existing_blog.image.save(image.name, image)
            print(f"Updated image to: {image.name}")

        if tags:
            try:
                tags_list = json.loads(tags)
                existing_blog.tags.clear()
                existing_blog.tags.add(*tags_list)
                print(f"Updated tags to: {tags_list}")
            except json.JSONDecodeError:
                return 400, {"message": "Invalid tags format"}

        existing_blog.save()
        print("Blog saved successfully")

        return 200, {
            "id": existing_blog.id,
            "title": existing_blog.title,
            "content": existing_blog.content,
            "image": existing_blog.image.url if existing_blog.image else None,
            "author": existing_blog.author.username,
            "category": existing_blog.category.title if existing_blog.category else None,
            "tags": [tag.name for tag in existing_blog.tags.all()],
            "created_at": existing_blog.created_at,
            "is_active": existing_blog.is_active
        }
    except Exception as e:
        print(f"Error updating blog: {str(e)}")
        return 400, {"message": str(e)}


def delete_blog(request, blog_id: int):
    blog = get_object_or_404(Blog, id=blog_id)

    if blog.author != request.auth:
        return 403, {"message": "You can only delete your own blogs"}

    blog.delete()
    return 204, None


def list_blog_comments(request, blog_id: int):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = Comment.objects.filter(blog=blog, parent=None).prefetch_related('children')

    return {
        "count": comments.count(),
        "results": [
            {
                "id": comment.id,
                "content": comment.content,
                "author": comment.author.username,
                "blog_id": blog_id,
                "parent_id": comment.parent_id,
                "created_at": comment.created_at,
                "likes": comment.likes,
                "dislikes": comment.dislikes,
                "children": [
                    {
                        "id": child.id,
                        "content": child.content,
                        "author": child.author.username,
                        "blog_id": blog_id,
                        "parent_id": child.parent_id,
                        "created_at": child.created_at,
                        "likes": child.likes,
                        "dislikes": child.dislikes,
                        "children": []
                    }
                    for child in comment.children.all()
                ]
            }
            for comment in comments
        ]
    }


def create_comment(request, blog_id: int, data: CommentCreateSchema):
    blog = get_object_or_404(Blog, id=blog_id)

    parent = None
    if data.parent_id and data.parent_id != 0:
        try:
            parent = Comment.objects.get(id=data.parent_id, blog=blog)
        except Comment.DoesNotExist:
            return 400, {"message": "Parent comment not found"}

    comment = Comment.objects.create(
        content=data.content,
        blog=blog,
        author=request.auth,
        parent=parent
    )

    return 201, {
        "id": comment.id,
        "content": comment.content,
        "author": comment.author.username,
        "blog_id": blog_id,
        "parent_id": comment.parent.id if comment.parent else None,
        "created_at": comment.created_at,
        "likes": 0,
        "dislikes": 0,
        "children": []
    }


def update_comment(request, blog_id: int, comment_id: int, data: CommentUpdateSchema):
    try:
        comment = get_object_or_404(Comment, id=comment_id, blog_id=blog_id)

        if comment.author != request.auth:
            return 403, {"message": "Not authorized to update this comment"}

        comment.content = data.content
        comment.save()

        return 200, {
            "id": comment.id,
            "content": comment.content,
            "author": comment.author.username,
            "blog_id": comment.blog_id,
            "parent_id": comment.parent.id if comment.parent else None,
            "created_at": comment.created_at
        }
    except Exception as e:
        return 400, {"message": str(e)}


def delete_comment(request, blog_id: int, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id, blog_id=blog_id)

    if comment.author != request.auth:
        return 403, {"message": "Not authorized to delete this comment"}

    comment.delete()
    return 204, None


def list_categories(request):
    categories = Category.objects.filter(parent=None).prefetch_related('children')

    def get_category_dict(category):
        return {
            "id": category.id,
            "title": category.title,
            "parent_id": category.parent_id,
            "children": [get_category_dict(child) for child in category.children.all()]
        }

    category_list = [get_category_dict(category) for category in categories]

    return {
        "count": len(category_list),
        "results": category_list
    }


def get_category(request, category_id: int):
    category = get_object_or_404(Category, id=category_id)

    def get_category_dict(cat):
        return {
            "id": cat.id,
            "title": cat.title,
            "parent_id": cat.parent_id,
            "children": [get_category_dict(child) for child in cat.children.all()]
        }

    return get_category_dict(category)


def like_comment(request, blog_id: int, comment_id: int):
    try:
        comment = get_object_or_404(Comment, id=comment_id, blog_id=blog_id)
        comment.likes += 1
        comment.save()

        children = comment.children.all()
        children_data = [
            {
                "id": child.id,
                "content": child.content,
                "author": child.author.username,
                "blog_id": child.blog_id,
                "parent_id": child.parent.id if child.parent else None,
                "created_at": child.created_at,
                "likes": child.likes,
                "dislikes": child.dislikes,
                "children": []
            }
            for child in children
        ]

        return 200, {
            "id": comment.id,
            "content": comment.content,
            "author": comment.author.username,
            "blog_id": comment.blog_id,
            "parent_id": comment.parent.id if comment.parent else None,
            "created_at": comment.created_at,
            "likes": comment.likes,
            "dislikes": comment.dislikes,
            "children": children_data
        }
    except Exception as e:
        return 400, {"message": str(e)}


def dislike_comment(request, blog_id: int, comment_id: int):
    try:
        comment = get_object_or_404(Comment, id=comment_id, blog_id=blog_id)
        comment.dislikes += 1
        comment.save()

        children = comment.children.all()
        children_data = [
            {
                "id": child.id,
                "content": child.content,
                "author": child.author.username,
                "blog_id": child.blog_id,
                "parent_id": child.parent.id if child.parent else None,
                "created_at": child.created_at,
                "likes": child.likes,
                "dislikes": child.dislikes,
                "children": []
            }
            for child in children
        ]

        return 200, {
            "id": comment.id,
            "content": comment.content,
            "author": comment.author.username,
            "blog_id": comment.blog_id,
            "parent_id": comment.parent.id if comment.parent else None,
            "created_at": comment.created_at,
            "likes": comment.likes,
            "dislikes": comment.dislikes,
            "children": children_data
        }
    except Exception as e:
        return 400, {"message": str(e)}


def list_categories(request):
    categories = Category.objects.filter(parent=None).prefetch_related('children')

    def get_category_dict(category):
        return {
            "id": category.id,
            "title": category.title,
            "parent_id": category.parent_id,
            "children": [get_category_dict(child) for child in category.children.all()]
        }

    category_list = [get_category_dict(category) for category in categories]

    return {
        "count": len(category_list),
        "results": category_list
    }


def get_category(request, category_id: int):
    category = get_object_or_404(Category, id=category_id)

    def get_category_dict(cat):
        return {
            "id": cat.id,
            "title": cat.title,
            "parent_id": cat.parent_id,
            "children": [get_category_dict(child) for child in cat.children.all()]
        }

    return get_category_dict(category)
