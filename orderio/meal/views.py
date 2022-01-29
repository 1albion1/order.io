from django.shortcuts import get_object_or_404, render,redirect
from meal.models import Meal,Category
from django.contrib import messages
from main.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm,MealForm
# Create your views here.


@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def create_meal(request):
    form = MealForm()
    if request.method == 'POST':
        form = MealForm(request.POST,request.FILES,)
        if form.is_valid():
            messages.success(request,f"Meal {request.POST.get('name')} was created successfully!")
            form.save()
            return redirect("meal:create_meal")
            
    context = {"form":form}
    return render(request,"meal/create_meal.html",context)

def view_meal(request,pk):
    meal = get_object_or_404(Meal,pk=pk)
    context = {"meal":meal}
    return render(request,"meal/view_meal.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def all_meals(request):
    meals = Meal.objects.all()
    context = {"meals":meals}
    return render(request,"meal/all_meals.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def update_meal(request,pk):
    meal = get_object_or_404(Meal,pk=pk)
    form = MealForm(instance=meal)
    if request.method == 'POST':
        form = MealForm(request.POST,request.FILES,instance=meal)
        if form.is_valid():
            messages.success(request,f"Meal {request.POST.get('name')} was updated successfully!")
            form.save()
            return redirect("meal:all_meals")
    context = {"form":form}
    return render(request,"meal/update_meal.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def delete_meal(request,pk):
    meal = get_object_or_404(Meal,pk=pk)
    meal.delete()
    messages.success(request,"The meal was deleted successfully!")
    return redirect("meal:all_meals")

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def create_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            messages.success(request,f"Category {request.POST.get('name')} was created successfully!")
            form.save()
            return redirect("meal:all_categories")
    context = {"form":form}
    return render(request,"meal/create_category.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def view_category(request,pk):
    category = get_object_or_404(Category,pk=pk)
    context = {"category":category}
    return render(request,"meal/view_category.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def all_categories(request):
    categories = Category.objects.all()
    context = {"categories":categories}
    return render(request,"meal/all_categories.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def update_category(request,pk):
    category = get_object_or_404(Category,pk=pk)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            messages.success(request,f"Category {request.POST.get('name')} was updated successfully!")
            form.save()
            return redirect("meal:all_categories")
    context = {"form":form}
    return render(request,"meal/update_category.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def delete_category(request,pk):
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,"Category was deleted successfully!")
    return redirect("meal:all_categories")