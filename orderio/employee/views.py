from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404
from main.forms import UserProfileForm
from main.decorators import allowed_users
from main.session_handle import Custom_Session
from django.http.response import JsonResponse
from django.contrib import messages
from meal.models import Meal
from menu.models import Menu,WeeklyMenu
from django.utils import timezone
from employee.employee_status import *
from employee.models import Employee
from django.http.response import HttpResponse
# Create your views here.
year = timezone.now().isocalendar().year
@login_required(login_url="login")
@allowed_users(allowed_roles=['user'])
def index(request):
    week = timezone.now().isocalendar().week
    
    budget_available = user_money_available(request)
    context = {"budget_available":budget_available,"week":week,"year":year}
    return render(request,'employee/index.html',context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['user'])
def employee_profile(request):
    employee = request.user.employee
    e_form = UserProfileForm(instance=employee)
    if request.method == 'POST':
        e_form = UserProfileForm(request.POST,request.FILES,instance = employee)
        if e_form.is_valid():
            e_form.save()
            messages.success(request,"Profile changes were saved successfully!")
    context = {"e_form":e_form}
    return render(request,'employee/employee_profile.html',context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['user'])
def daily_menu(request):
    week = timezone.now().isocalendar().week
    day = timezone.now().isoweekday()
    menu_budget = user_money_available(request)
    try:
        weekly_menu = get_object_or_404(WeeklyMenu,week=week,year=year)
        menu = weekly_menu.menu_set.get(created_for=day)
        menu_status = "Available" if menu.allowes_orders() else "Expired"
        print(menu_status)
        if not menu.approved:
            return HttpResponse("The menu for today is not approved ready yet!")
    except:
        return HttpResponse(f"The menu for today is not ready yet!")
    meals = menu.meals.all()
    context={"menu":menu,"meals":meals,"day":day,"menu_status":menu_status,"menu_budget":menu_budget}
    return render(request,'employee/daily_menu.html',context)
    
def change_daily_allowance(request,pk):
    employee = get_object_or_404(Employee,pk=pk)
    if request.method == 'POST':
        employee.daily_allowance = request.POST.get('daily_allowance')
        employee.save()
        messages.success(request,f"Daily allowance changed for user {employee.user.username}")
    return redirect("user_list")

