from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from main.forms import UserProfileForm
from main.decorators import allowed_users
from main.session_handle import Custom_Session
from django.http.response import JsonResponse
from django.contrib import messages
from meal.models import Meal
from menu.models import Menu,WeeklyMenu
from django.utils import timezone
from employee.employee_status import *
# Create your views here.
@login_required(login_url="login")
@allowed_users(allowed_roles=['user'])
def index(request):
    budget_available = user_money_available(request)
    context = {"budget_available":budget_available}
    return render(request,'user/index.html',context)

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
def add_to_order(request):
    ss = Custom_Session(request)
    if request.POST.get('action') == 'add':
        meal_id = int(request.POST.get('meal_id'))
        meal = get_object_or_404(Meal,pk=meal_id)
        ss.add(product=meal)
        response = JsonResponse({"id": meal.id})
        return response
    if request.POST.get('action') == 'remove':
        meal_id = str(request.POST.get('meal_id'))
        ss.remove(product=meal_id)
        response = JsonResponse({"id": meal_id})
        return response
    
