from .models import Menu
def menu_capacity(request):
    try:
        capacity = Menu.CAPACITY
    except:
        capacity = 7
    return {"menu_cap":capacity,}
