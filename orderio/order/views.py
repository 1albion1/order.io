from django.http import Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.template import context
from main.decorators import allowed_users 
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from menu.models import Menu,WeeklyMenu
from main.session_handle import Custom_Session
from .models import Order
from employee.models import Employee
from django.contrib import messages
from django.utils import timezone
from employee.employee_status import can_user_order
from meal.models import Meal
from order.filters import OrderFilter
from notification.models import Notification
from order.forms import OrderCreationForm
# Create your views here.
# Create your views here.
@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def daily_orders(request):
    week = timezone.now().isocalendar().week
    day = timezone.now().isoweekday()
    year = timezone.now().isocalendar().year
    try:
        weekly_menu = get_object_or_404(WeeklyMenu,week=week,year=year)
        menu = weekly_menu.menu_set.get(created_for=day)
        orders = menu.order_set.all()
        if not menu.approved:
            return render(request,'manager/error-template.html',{"text":f"You have not approved today's menu! Go to 'This week\'s menu' and approve the menu for {menu.get_day_name()}"})
        context={"orders":orders,"day":menu.get_day_name,"week":week,"year":year}
        return render(request,"order/daily_orders.html",context)

    except:
        return render(request,'manager/error-template.html',{"text":"You have not created a menu for today!"})

    
@login_required(login_url="login")
@allowed_users(allowed_roles=['user'])
def create_order(request):
    ss = Custom_Session(request)
    employee = get_object_or_404(Employee,user=request.user.id)
    if request.method == "POST":
        menu = get_object_or_404(Menu,id=request.POST.get('menu_id'))
        if menu.allowes_orders():
            if can_user_order(request,ss.get_total_price()):
                meals = ss.get_menu_items()

                for meal in meals.keys():
                    if not menu.meals.filter(pk=meal):
                        ss.clear()
                        return HttpResponse("the meal is not on the menu")
                total_price = ss.get_total_price()
                order = Order(employee = employee, menu=menu,order_cost=total_price)
                order.save()
                order.meals.set(meals)
                order.save()
                ss.clear()
                messages.success(request,"Your order was created successfully!")
            else:
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request,"Menu does not allow orders anymore")
            return redirect("employee:index")
    return redirect("employee:index")

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def view_order(request,pk):
    order = get_object_or_404(Order,pk=pk)
    context ={"order" : order}
    return render(request,'order/view_order.html',context)

def user_order_history(request):
    orders = Order.objects.filter(employee = request.user.employee)
    
    context={
        "orders":orders
    }
    return render(request,"employee/order_history.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def change_order_status(request,pk,status):
    order = get_object_or_404(Order,pk=pk)
    if status == 1:
        order.order_status = "Accepted"
    elif status == 0:
        order.order_status = "Denied"
    else: 
        return redirect("order:daily_orders")
    order.save()
    type = 0 if order.order_status == "Denied" else 1
    Notification(to_user=order.employee.user,from_user=request.user,text=f"Your order for {order.menu.get_day_name()} was {order.order_status}",type=type).save()
    return redirect("order:daily_orders")

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

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def all_orders_this_week(request):
    week = timezone.now().isocalendar().week
    year = timezone.now().isocalendar().year
    weekly_menu = get_object_or_404(WeeklyMenu,week=week,year=year)
    orders = Order.objects.filter(created_at__week=week)
    if request.method == "GET":    
        order_filter = OrderFilter(request.GET,queryset=orders)
        orders = order_filter.qs
    context = {"weekly_menu":weekly_menu,"order_filter":order_filter,"orders":orders,"week":week,"year":year}
    return render(request,"order/all_orders_this_week.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def full_order_history(request):
    orders = Order.objects.all()
    context = {"orders":orders}
    if request.method == "GET":    
        order_filter = OrderFilter(request.GET,queryset=orders)
        orders = order_filter.qs
    context = {"order_filter":order_filter,"orders":orders}
    return render(request,"order/full_order_history.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def custom_order(request):
    form = OrderCreationForm()
    if request.method == "POST":
        order_form = OrderCreationForm(request.POST)
        if order_form.is_valid():
            order = order_form.save()
            meals = request.POST.getlist('meals')
            order.meals.set(meals)
            order.save()
            messages.success(request,"Custom order created successfully!")
            return redirect("manager:index")
        
    context = {"form":form}
    return render(request,"order/custom_order.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['user'])
def delete_order(request,pk):
    order = get_object_or_404(Order,pk=pk)
    if order.employee == request.user.employee:
        if order.order_status == 'Pending':
            order.delete()
            messages.success(request,"Order was deleted successfully! You can now make a new order.")
        else:
            messages.warning(request,"You can only cancel orders that are pending!")
            return redirect("employee:index")
    else:
        return HttpResponse("You cannot delete this order!")
    return redirect("employee:index")