from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.session_handle import Custom_Session
from main.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from main.forms import CreateUserForm,EmployeeForm
from django.contrib import messages
from django.utils import timezone
from menu.models import WeeklyMenu,Menu
from meal.models import Meal

#weekly menu
@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def weekly_menu(request):
    week = timezone.now().isocalendar().week
    days = {1:"Moday",2:"Tuesday",3:"Wendnesday",4:"Thursday",5:"Friday",6:"Saturday",7:"Sunday"} 
    try:
        weekly_menu = WeeklyMenu.objects.get(week=week)
    except:
        weekly_menu = WeeklyMenu(week=week)
        weekly_menu.save()
        for day in Menu.DAYS:
            if day[0] in (6,7):
                menu = Menu.objects.create(weekly_menu = weekly_menu,created_for=day[0],is_holiday=True)
                menu.save()
            else:
                menu = Menu.objects.create(weekly_menu = weekly_menu,created_for=day[0])
                menu.save()
    menus = weekly_menu.menu_set.all()
    context={"weekly_menu":weekly_menu,"menus":menus,"days":days}
    return render(request,'menu/weekly_menu.html',context)

def all_weekly_menus(request):
    all_weekly_menus = WeeklyMenu.objects.all()
    context={"all_weekly_menus":all_weekly_menus}
    return render(request,"menu/all_weekly_menus.html",context)

def weekly_menu_all_orders(request,pk):
    wm = get_object_or_404(WeeklyMenu,pk=pk)
    orders = wm.order_set.all()
    context = {"orders":orders}
    return render(request,"menu/weekly_menu_all_orders.html",context)

def view_weekly_menu(request,pk):
    wm = get_object_or_404(WeeklyMenu,pk=pk)


@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def update_menu(request,pk):
    meals = Meal.objects.all()
    menu = get_object_or_404(Menu,pk=pk)
    menu_meals = menu.meals.all()
    item_count = menu.meals.all().count()
    item_price_total = menu.get_menu_total_price()
    

    if request.method == 'POST':
        avability = request.POST.get("avability")
        menu.avability = avability
        menu.save()
        messages.success(request,"Menu has been saved!")
        return redirect("menu:weekly_menu")
    context = {"menu":menu,"menu_meals":menu_meals,"meals":meals,"item_count":item_count,"item_price_total":item_price_total,}
    return render(request,"menu/update_menu.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def approve_menu(request,pk):
    menu = get_object_or_404(Menu,pk=pk)
    menu.approved = True
    menu.approved_at = timezone.now()
    menu.save()
    return redirect("menu:weekly_menu")

def view_menu(request,pk):
    menu = get_object_or_404(Menu,pk=pk)
    context = {"menu":menu}
    return render(request,"menu/view_menu.html",context)

def make_menu_holiday(request,pk):
    menu = get_object_or_404(Menu,pk=pk)
    menu.is_holiday = False if menu.is_holiday else True
    menu.save()
    return redirect("menu:weekly_menu")

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def add_to_menu(request,meal_pk,menu_pk):
    menu = get_object_or_404(Menu,pk=menu_pk)
    meal = get_object_or_404(Meal,pk=meal_pk)
    menu.meals.add(meal)
    print(menu.meals.all())
    return redirect("menu:update_menu",pk=menu_pk)
    
def remove_from_menu(request,meal_pk,menu_pk):
    menu = get_object_or_404(Menu,pk=menu_pk)
    meal = get_object_or_404(Meal,pk=meal_pk)
    menu.meals.remove(meal)
    return redirect("menu:update_menu",pk=menu_pk)
    

    
