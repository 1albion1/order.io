from order.models import Order
from menu.models import Menu, WeeklyMenu
from django.utils import timezone
from django.contrib import messages
today = timezone.now().date()
week = timezone.now().isocalendar().week

def has_order(request):
    user_orders = Order.objects.filter(created_at__date = today, employee = request.user.employee)
    if user_orders:
        return True
    return False

def user_money_spent(request):
    employee = request.user.employee
    spent = 0
    weekly_menu = WeeklyMenu.objects.get(week=week)
    for menu in weekly_menu.menu_set.all():
        for order in menu.order_set.filter(employee=employee):
            spent += order.cost
    return spent

def allowance_until_now(request):
    weekly_menu = WeeklyMenu.objects.get(week=week)
    total_working_days = weekly_menu.menu_set.all()
    weekday = timezone.now().isoweekday()
    days_until_now = 0
    for day in total_working_days:
        if int(day.created_for) > weekday:
            break
        else:
            if not day.is_holiday:
                days_until_now += 1
    daily_allowance = request.user.employee.daily_allowance
    allowance_until_now = days_until_now*daily_allowance
    return allowance_until_now

def user_money_available(request):
    return allowance_until_now(request)-user_money_spent(request)


def can_user_order(request,cost):
    if not has_order(request):
        if cost>user_money_available(request):
            messages.warning(request,"You cannot afford the total cost of that order!")
            return False
        return True
    else:
        messages.warning(request,"You have already placed an order for today!")
        return False

