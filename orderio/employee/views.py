from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404
from main.forms import UserProfileForm,FnameLnameForm
from main.decorators import allowed_users
from main.session_handle import Custom_Session
from django.contrib import messages
from notification.models import Notification
from menu.models import WeeklyMenu
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
    day = timezone.now().isoweekday()
    day_name = timezone.now().strftime("%A")
    has_ordered = has_order(request)
    orders = Order.objects.filter(employee = request.user.employee)[:5]
    try:
        weekly_menu = WeeklyMenu.objects.get(week=week,year=year)
        menu = weekly_menu.menu_set.get(created_for=day)
        
    except:
        menu = ""
       
    
    
    budget_available = user_money_available(request)
    context = {"budget_available":budget_available,
               "menu":menu,
               "day_name":day_name,
               "orders":orders,
               "has_ordered":has_ordered}
    return render(request,'employee/index.html',context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['user'])
def my_profile(request):
    employee = request.user.employee
    e_form = UserProfileForm(instance=employee)
    fl_form = FnameLnameForm(instance=request.user)
    if request.method == 'POST':
        e_form = UserProfileForm(request.POST,request.FILES,instance = employee)
        fl_form = FnameLnameForm(request.POST,instance=request.user)
        if e_form.is_valid() and fl_form.is_valid():
            e_form.save()
            fl_form.save()
            messages.success(request,"Profile changes were saved successfully!")
            return redirect("employee:index")
    context = {"e_form":e_form,"fl_form":fl_form}
    return render(request,'employee/employee_profile.html',context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['user'])
def daily_menu(request):
    ss = Custom_Session(request)
    day = timezone.now().isoweekday()
    menu_budget = user_money_available(request)
    try:
        weekly_menu = WeeklyMenu.objects.get(week=week,year=year)
        menu = weekly_menu.menu_set.get(created_for=day)
        menu_status = "Available" if menu.allowes_orders() else "Expired"
        if not menu.approved:
            return render(request,'employee/error-template.html',{"text":f"The menu for {menu.get_day_name()} is not approved ready yet!"})
        meals = menu.meals.all()
        for meal in ss.get_menu_items():
            meals=meals.exclude(pk=meal)
        
        context={"menu":menu,"meals":meals,"day":day,"menu_status":menu_status,"menu_budget":menu_budget,"week":week,"year":year}
        return render(request,'employee/daily_menu.html',context)
    except:
        return render(request,'employee/error-template.html',{"text":f"The menu for today is not ready yet!"})

    
    
@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def change_daily_allowance(request,pk):
    employee = get_object_or_404(Employee,pk=pk)
    
    if request.method == 'POST':
        if not has_order_this_week(request,pk):
            employee.daily_allowance = request.POST.get('daily_allowance')
            employee.save()
            Notification(to_user=employee.user,from_user=request.user,text=f"Your daily allowance was changed to {float(request.POST.get('daily_allowance'))}",type=2).save()
            messages.success(request,f"Daily allowance changed for user {employee.user.username}")
        else:
            messages.warning(request,f"You cannot change the allowance for this user. Make sure the user has not placed an order yet!")
            return redirect("user_list")
    return redirect("user_list")

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def employee_profile(request,pk):
    employee = get_object_or_404(Employee,user=pk)
    
    
    context = {"employee":employee}
    return render(request,'employee/public_profile.html',context)