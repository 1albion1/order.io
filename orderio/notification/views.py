from django.http.response import JsonResponse
from django.shortcuts import render,get_object_or_404,redirect
from .models import Notification
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
# Create your views here.

@login_required(login_url="login")
@allowed_users(allowed_roles=['user'])
def notif_seen(request):
    if request.method == "POST":
        pk = int(request.POST.get('notification_pk'))
        notification = get_object_or_404(Notification,pk=pk)
        notification.seen = True
        notification.save()
    response = JsonResponse({"status": "saved"})
    return response

@login_required(login_url="login")
@allowed_users(allowed_roles=['user'])
def clear_notifications(request):
    notifications = Notification.objects.filter(to_user=request.user)
    for notification in notifications:
        notification.delete()
    return redirect(request.META.get('HTTP_REFERER'))