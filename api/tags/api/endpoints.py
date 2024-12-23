from django.db.models import Count
from taggit.models import Tag


def list_tags(request):
    tags = Tag.objects.annotate(count=Count('taggit_taggeditem_items')).order_by('-count', 'name')
    return [
        {
            "id": tag.id,
            "name": tag.name,
            "count": tag.count
        }
        for tag in tags
    ]