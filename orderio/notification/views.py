from django.http.response import JsonResponse
from django.shortcuts import render,get_object_or_404
from .models import Notification
# Create your views here.

def notif_seen(request):
    if request.method == "POST":
        pk = int(request.POST.get('notification_pk'))
        notification = get_object_or_404(Notification,pk=pk)
        notification.seen = True
        notification.save()
    response = JsonResponse({"status": "saved"})
    return response