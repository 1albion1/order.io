from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404
from main.forms import UserProfileForm,FnameLnameForm
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
week = timezone.now().isocalendar().week
@login_required(login_url="login")
@allowed_users(allowed_roles=['user'])
def index(request):
    budget_available = user_money_available(request)
    context = {"budget_available":budget_available,"week":week,"year":year}
    return render(request,'employee/index.html',context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['user'])
def employee_profile(request):
    employee = request.user.employee
    e_form = UserProfileForm(instance=employee)
    fl_form = FnameLnameForm(instance=request.user)
    if request.method == 'POST':
        e_form = UserProfileForm(request.POST,request.FILES,instance = employee)
        fl_form = FnameLnameForm(request.POST,instance=request.user)
        if e_form.is_valid() and fl_form.is_valid:
            e_form.save()
            fl_form.save()
            messages.success(request,"Profile changes were saved successfully!")
            return redirect("employee:index")
    context = {"e_form":e_form,"fl_form":fl_form}
    return render(request,'employee/employee_profile.html',context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['user'])
def daily_menu(request):
    day = timezone.now().isoweekday()
    menu_budget = user_money_available(request)
    try:
        weekly_menu = WeeklyMenu.objects.get(week=week,year=year)
        menu = weekly_menu.menu_set.get(created_for=day)
        menu_status = "Available" if menu.allowes_orders() else "Expired"
        if not menu.approved:
            return HttpResponse(f"The menu for {menu.get_day_name} is not approved ready yet!")
        meals = menu.meals.all()
        context={"menu":menu,"meals":meals,"day":day,"menu_status":menu_status,"menu_budget":menu_budget,"week":week,"year":year}
        return render(request,'employee/daily_menu.html',context)
    except:
        return HttpResponse(f"The menu for today is not ready yet!")
    
    
    
def change_daily_allowance(request,pk):
    today = timezone.now().isoweekday()
    employee = get_object_or_404(Employee,pk=pk)
    
    if request.method == 'POST':
        if not has_order_this_week(request,pk):
            employee.daily_allowance = request.POST.get('daily_allowance')
            employee.save()
            messages.success(request,f"Daily allowance changed for user {employee.user.username}")
        else:
            return HttpResponse("This user already has an order this week. You cannot change the allowance!")
    return redirect("user_list")

