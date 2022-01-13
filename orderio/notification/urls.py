from django.urls import path
from . import views


app_name = "notification"
urlpatterns = [
    path("notif_seen",views.notif_seen,name="notif_seen"),
    path("clear_notifications",views.clear_notifications,name="clear_notifications"),
]
