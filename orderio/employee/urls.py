from django.urls import path
from . import views
app_name = "employee"
urlpatterns = [
    path("",views.index,name="index"),
    path("my_profile",views.my_profile,name="my_profile"),
    path("change_daily_allowance/<int:pk>",views.change_daily_allowance,name="change_daily_allowance"),
    path("daily_menu",views.daily_menu,name="daily_menu"),
    path("<int:pk>",views.employee_profile,name="employee_profile"),
    #path("delete_employee",views.delete_employee,name="delete_employee")
    #path("update_employee",views.update_employee,name="update_employee")
]
