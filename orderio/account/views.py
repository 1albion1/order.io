from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate,login,logout
from main.decorators import authenticated_user,allowed_users
from django.contrib import messages
from main.forms import  CreateUserForm,EmployeeForm
from main.session_handle import Custom_Session
from account.models import CustomUser,Role
from employee.models import Employee,Department
from django.contrib.auth.decorators import login_required
from notification.models import Notification
# Create your views here.

@authenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            try:
                if user.role.name == "manager":
                    return redirect("manager:index")
                else:
                    return redirect("employee:index")
            except:
                return render(request,'main/error-template.html',{"text":"Your user role was not found. Please contact the system admistrator to specify your role."})
        else:
            messages.warning(request,"Username or password is incorrect!")
    context = {}
    return render(request,"account/login.html",context)



@authenticated_user
def register(request):
    form = CreateUserForm()
    departments = Department.objects.all()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            department = get_object_or_404(Department,pk=request.POST.get("department")) 
            user = form.save(commit=False)
            try:
                Role.objects.get(name="user")
            except:
                role = Role(name="user")
                role.save()
            basic_role = Role.objects.get(name="user")
            user.role = basic_role
            user.save()
            Notification(to_user=user,text=f"Thank you for signing up to order.io! Make sure to complete your profile.",type=3).save()
            Employee.objects.create(user=user,department=department)
            username = form.cleaned_data['username']
            messages.success(request,f"Account for {username} has been created successfully!")
            return redirect("login")
    context = {"form":form,"departments":departments}
    return render(request,"account/register.html",context)

def logout_user(request):
    ss = Custom_Session(request)
    ss.clear()
    logout(request)
    return redirect("login")

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def create_user(request):
    form = CreateUserForm()
    groups = Role.objects.all()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            role = request.POST.get("role")
            if role:
                user = form.save()
                if user.role.name == "user":
                    Employee.objects.create(user=user)
                username = form.cleaned_data['username']
                messages.success(request,f"Account for {username} has been created successfully!")
                return redirect("manager:index")
            else:
                messages.warning(request,"You did not select a user type")    
    context = {"form":form,"groups":groups}
    return render(request,"account/create_user.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def user_list(request):
    users = CustomUser.objects.all()
    
    context ={"users":users}
    return render(request,"account/user_list.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def delete_user(request,pk):
    user = get_object_or_404(CustomUser,pk=pk)
    username = user.username
    user.delete()
    messages.success(request,f"{username} was deleted successfully.")
    return redirect("user_list")

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def update_user(request,pk):
    user = get_object_or_404(CustomUser,pk=pk)
    role = user.role.name
    if role == "user":
        employee = user.employee
        form = EmployeeForm(instance = employee)
    elif role == "manager":
        form = CreateUserForm(instance=user)
    else:
        return HttpResponse("User role not found!")
    if request.method == "POST":
        form = EmployeeForm(request.POST,instance = employee)
        if form.is_valid():
            form.save()
            messages.success(request,"Changes saved!")
            
    context={"user":user,"form":form}
    return render(request,"account/update_user.html",context)

