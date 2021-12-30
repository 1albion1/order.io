from django.urls import path
from . import views
app_name = "manager"
urlpatterns = [
    #index
    path("",views.index, name="index"),
    

    
]
