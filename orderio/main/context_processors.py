from .session_handle import Custom_Session
from django.shortcuts import  reverse
from django.utils import timezone
def bag(request):
    return {"bag":Custom_Session(request)}

def weekly_menu_link(request):
    year = timezone.now().isocalendar().year
    week = timezone.now().isocalendar().week
    return {"weekly_menu_link":reverse('menu:view_weekly_menu',kwargs={"week":week,"year":year})}