from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render,redirect
from main.decorators import allowed_users
from employee.models import Employee,Department
from account.models import CustomUser
from menu.models import WeeklyMenu
from django.urls import reverse
from django.http import JsonResponse

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def index(request):
    return render(request,'manager/index.html')


def reports_index (request):
    return render(request,'manager/reports_index.html')

def user_spendings(request):
    users = CustomUser.objects.filter(role__name = "user")
    context ={"users":users}
    return render(request,"manager/user_spendings.html",context)

def population_chart(request,pk):
    user = get_object_or_404(CustomUser,pk=pk)
    weekly_menus = WeeklyMenu.objects.all()
    total_spent = 0
    labels = []
    data = []
    
    for weekly_menu in weekly_menus.order_by('created_at')[:30]:
        for order in user.employee.order_set.filter(menu__weekly_menu = weekly_menu):
            total_spent+=order.order_cost
        labels.append(f'Week: {weekly_menu.week} {weekly_menu.year}')
        data.append(total_spent)
        total_spent=0
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
    
def total_orders_by_department(request):
    weekly_menus = WeeklyMenu.objects.all()
    context = {"weekly_menus":weekly_menus}
    return render(request,"manager/total_orders_by_department.html",context)

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