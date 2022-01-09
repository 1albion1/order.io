from order.models import Order
from django.shortcuts import get_object_or_404
from django.utils import timezone
from menu.models import WeeklyMenu

def pending_orders(request):
    week = timezone.now().isocalendar().week
    day = timezone.now().isoweekday()
    year = timezone.now().isocalendar().year
    try:
        weekly_menu = get_object_or_404(WeeklyMenu,week=week,year=year)
        menu = weekly_menu.menu_set.get(created_for=day)
        pending_orders = menu.order_set.filter(order_status="Pending").count()
    except:
        pending_orders = 0

    return {"pending_orders":pending_orders}