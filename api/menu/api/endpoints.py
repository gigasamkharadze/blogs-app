from menu.models import Menu

def get_menu(request):
    menu_items = Menu.objects.all().order_by('order')

    return {
        "items": [
            {
                "id": item.id,
                "title": item.title,
                "url": item.url,
                "order": item.order
            }
            for item in menu_items
        ]
    }
