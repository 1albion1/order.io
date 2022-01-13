from .models import Notification
def notifications(request):
    try:
        user = request.user.pk
    except:
        user = ""
    notifications = Notification.objects.filter(to_user=user)
    unseen = notifications.filter(seen=False).count()
    return {"notifications":notifications[:5],"unseen":unseen}
