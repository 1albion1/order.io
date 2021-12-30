from django.shortcuts import get_object_or_404, render
from main.models import *
from main.session_handle import Custom_Session
from main.decorators import *
from django.contrib.auth.decorators import login_required
from main.forms import CreateUserForm,EmployeeForm
from django.contrib.auth.models import Group
from user.models import Employee
from django.utils import timezone
from .models import *
from account.models import User,Role
from django.urls import reverse

def clear_session_update(request,pk):
    user_session = Custom_Session(request)
    user_session.clear()
    menu = get_object_or_404(Menu,pk=pk)
    menu_meals = menu.meals.all()
    for meal in menu_meals:
        user_session.add(product=meal)
    return redirect(reverse("manager:update_menu",kwargs={"pk":pk}))

def clear_session_create(request,pk):
    user_session = Custom_Session(request)
    user_session.clear()
    
    return redirect(reverse("manager:create_menu",kwargs={"weekly_id":pk}))