from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render,redirect
from main.session_handle import Custom_Session
from main.decorators import allowed_users
from menu.models import Menu
from django.urls import reverse

@login_required(login_url="login")
@allowed_users(allowed_roles=['manager'])
def index(request):
    return render(request,'manager/index.html')

