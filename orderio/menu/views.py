from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render,reverse
from main.session_handle import Custom_Session
from main.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from menu.models import WeeklyMenu,Menu
from meal.models import Meal
from menu.custom_functions import user_or_manager
#weekly menu
@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def weekly_menu(request):
    week = timezone.now().isocalendar().week
    year = timezone.now().isocalendar().year

    try:
        weekly_menu = WeeklyMenu.objects.get(week=week,year=year)
    except:
        weekly_menu = WeeklyMenu(week=week,year=year)
        weekly_menu.save()
    menus = weekly_menu.menu_set.all()
    context={"weekly_menu":weekly_menu,"menus":menus}
    return render(request,'menu/weekly_menu.html',context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def all_weekly_menus(request):
    all_weekly_menus = WeeklyMenu.objects.all()
    context={"all_weekly_menus":all_weekly_menus}
    return render(request,"menu/all_weekly_menus.html",context)

@login_required(login_url="login")
def view_weekly_menu(request,week,year):
    try:
        wm = WeeklyMenu.objects.get(week=week,year=year)
    except:
        wm = ""
    context = {"wm":wm}
    return user_or_manager(request,"view_weekly_menu",context)
    
@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def delete_menu(request,pk):
    menu = get_object_or_404(Menu,pk=pk)
    name = menu.get_day_name()
    menu.delete()
    messages.success(request,f"Menu for {name} was deleted successfully!")
    return redirect("menu:weekly_menu")
    
#daily menu
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
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def view_menu(request,pk):
    menu = get_object_or_404(Menu,pk=pk)
    context = {"menu":menu}
    return render(request,f"menu/view_menu.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def add_to_menu(request,meal_pk,menu_pk):
    print(meal_pk)
    menu = get_object_or_404(Menu,pk=menu_pk)
    meal = get_object_or_404(Meal,pk=meal_pk)
    item_count = menu.meals.all().count()
    if item_count >= Menu.CAPACITY:
            messages.warning(request,f"You cannot add more than {Menu.CAPACITY} meals")
            return redirect(reverse("menu:update_menu",kwargs={"pk":menu.pk}))
    menu.meals.add(meal)
    return redirect("menu:update_menu",pk=menu_pk)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def remove_from_menu(request,meal_pk,menu_pk):
    menu = get_object_or_404(Menu,pk=menu_pk)
    meal = get_object_or_404(Meal,pk=meal_pk)
    menu.meals.remove(meal)
    return redirect("menu:update_menu",pk=menu_pk)
       
@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def index(request):
    return render(request,'manager/index.html')

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def create_menu(request,weekly_id):
    meals = Meal.objects.all()
    weekly_menu = get_object_or_404(WeeklyMenu,id=weekly_id) 
    all_options = Menu.DAYS
    available_options = []
    ss = Custom_Session(request)
    for meal in ss.get_menu_items():
        meals=meals.exclude(pk=meal)
    for day in all_options:
        if not weekly_menu.menu_set.filter(created_for=day[0]):
            available_options.append(int(day[0]))
    if request.method == 'POST':
        
        weekday = request.POST.get('weekday')
        menu_meals_session = ss.get_menu_items()
        if len(menu_meals_session) > Menu.CAPACITY:
            return HttpResponse(f"You cannot add more than {Menu.CAPACITY} meals")
        avability = request.POST.get('menu_avability')  
        
        if weekly_menu.menu_set.filter(created_for=weekday):
            return HttpResponse(f"A menu for {Menu.DAYS[int(weekday)-1][1]} has already been created!")
        else:
            menu = Menu(created_for=weekday,avability=avability,weekly_menu=weekly_menu)
            menu.save()
            menu.meals.set(menu_meals_session)
            menu.save()
            ss.clear()
            messages.success(request,f"Your menu for {Menu.DAYS[int(weekday)-1][1]} has been created!")
            return redirect("menu:weekly_menu")
    context = {
        "meals":meals,
        "available_options" : available_options,
        "all_options" : all_options
    }
    return render(request,"menu/create_menu.html",context)

    
@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def update_session(request):
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
        