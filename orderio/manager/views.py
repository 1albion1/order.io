from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from main.decorators import allowed_users
from employee.models import Department
from account.models import CustomUser
from menu.models import WeeklyMenu,Menu
from order.models import Order
from django.http import JsonResponse
from django.utils import timezone
from datetime import date
from meal.models import Meal

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def index(request):
    week = timezone.now().isocalendar().week
    day = timezone.now().isoweekday()
    year = timezone.now().isocalendar().year
    total_users = CustomUser.objects.filter(role__name="user").count()
    try:
        weekly_menu = get_object_or_404(WeeklyMenu,week=week,year=year)
        menu = weekly_menu.menu_set.get(created_for=day)
        
    except:
        menu = ""
    this_week_orders = Order.objects.filter(created_at__week=week).count()
    context= {
              "this_week_orders":this_week_orders,
              "menu":menu,
              "total_users":total_users,
              }
    return render(request,'manager/index.html',context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def reports_index (request):
    return render(request,'manager/reports_index.html')

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def user_spendings(request):
    users = CustomUser.objects.filter(role__name = "user")
    context ={"users":users}
    return render(request,"manager/user_spendings.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def chart_user_spendings(request,pk):
    user = get_object_or_404(CustomUser,pk=pk)
    weekly_menus = WeeklyMenu.objects.all()
    total_spent = 0
    labels = []
    data = []
    
    for weekly_menu in weekly_menus.order_by('created_at')[:30]:
        for order in user.employee.order_set.filter(menu__weekly_menu = weekly_menu):
            total_spent+=order.order_cost
        labels.append(str(weekly_menu))
        data.append(total_spent)
        total_spent=0
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def total_orders_by_department(request):
    weekly_menus = WeeklyMenu.objects.all()
    context = {"weekly_menus":weekly_menus}
    return render(request,"manager/total_orders_by_department.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def chart_total_orders_by_department(request,pk):
    weekly_menu = get_object_or_404(WeeklyMenu,pk=pk)
    labels = []
    data = []
    order_count = 0
    departments = Department.objects.all()
    for department in departments:
        for employee in department.employee_set.all():
            order_count+=employee.order_set.filter(menu__weekly_menu = weekly_menu).count()
        labels.append(department.name)
        data.append(order_count)
        order_count = 0
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
    
@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def most_ordered_meals(request):
    weekly_menus = WeeklyMenu.objects.all()
    context = {"weekly_menus":weekly_menus}
    return render(request,"manager/most_ordered_meals.html",context)

def chart_most_ordered_meals(request,pk):
    labels = []
    data = []
    if pk !=0:
        weekly_menu = get_object_or_404(WeeklyMenu,pk=pk)
    meals=Meal.objects.all()
    for meal in meals:
        labels.append(str(meal))
        if pk ==0:
            data.append(meal.order_set.all().count())
        else:
            data.append(meal.order_set.filter(menu__weekly_menu=weekly_menu).count())
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])   
def number_of_orders_by_day(request):
    labels = []
    data = []
    menus = Menu.objects.filter(approved=True).order_by('-weekly_menu','created_for',)[:20]
    for menu in menus:
        labels.append(str(date.fromisocalendar(menu.weekly_menu.year,menu.weekly_menu.week,menu.created_for,).strftime("%a, %d/%b/%y")))
        data.append(menu.order_set.all().count())
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })