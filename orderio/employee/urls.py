from django.urls import path
from . import views
app_name = "employee"
urlpatterns = [
    path("",views.index,name="index"),
    path("employee_profile",views.employee_profile,name="employee_profile"),
    path("add_to_order",views.add_to_order,name="add_to_order"),
    #path("delete_employee",views.delete_employee,name="delete_employee")
    #path("update_employee",views.update_employee,name="update_employee")
]
