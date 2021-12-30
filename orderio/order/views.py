from django.shortcuts import render,get_object_or_404,redirect
from main.decorators import allowed_users 
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from menu.models import Menu,WeeklyMenu
from main.session_handle import Custom_Session
from .models import Order
from employee.models import Employee
from django.contrib import messages
from django.utils import timezone
from employee.employee_status import *
# Create your views here.
# Create your views here.
@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def daily_orders(request):
    week = timezone.now().isocalendar().week
    day = timezone.now().isoweekday()
    try:
        weekly_menu = get_object_or_404(WeeklyMenu,week=week)
        menu = weekly_menu.menu_set.get(created_for=day)
        orders = menu.order_set.all()
        if not menu.approved:
            return HttpResponse("You have not approved today's menu!")
    except:
        return HttpResponse("You have not created a menu for today!")
    context={"orders":orders}
    return render(request,"order/daily_orders.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def weekly_orders(request):
    
    context={}
    return render(request,"order/weekly_orders.html",context)

def create_order(request):
    ss = Custom_Session(request)
    employee = get_object_or_404(Employee,user=request.user.id)
    if request.method == "POST":
        menu = get_object_or_404(Menu,id=request.POST.get('menu_id'))
        if menu.allowes_orders():
            if can_user_order(request,ss.get_total_price()):
                meals = ss.get_menu_items()
                total_price = ss.get_total_price()
                order = Order(employee = employee, menu=menu,order_cost=total_price)
                order.save()
                order.meals.set(meals)
                order.save()
                ss.clear()
                messages.success(request,"Your order was created successfully!")
            else:
                return redirect("user:index")
        else:
            messages.warning(request,"Menu does not allow orders anymore")
            return redirect("user:index")
        
    return redirect("user:index")



def view_order(request,pk):
    order = get_object_or_404(Order,pk=pk)
    context ={"order" : order}
    return render(request,'order/view_order.html',context)

def user_order_history(request):
    employee = get_object_or_404(Employee,user=request.user.id)
    orders = employee.order_set.all()
    
    context={
        "orders":orders
    }
    return render(request,"user/order_history.html",context)

def change_order_status(request,pk,status):
    order = get_object_or_404(Order,pk=pk)
    if status == 1:
        order.order_status = "Accepted"
    elif status == 0:
        order.order_status = "Denied"
    else: 
        return redirect("order:daily_orders")
    order.save()
    return redirect("order:daily_orders")