from django.urls import path
from . import views

app_name = "manager"
urlpatterns = [
    # path("create_menu/<int:weekly_id>/",views.create_menu,name="create_menu"),
    path("add_to_menu/<int:meal_pk>/<int:menu_pk>",views.add_to_menu,name="add_to_menu"),
    path("remove_from_menu/<int:meal_pk>/<int:menu_pk>",views.remove_from_menu,name="remove_from_menu"),
    path("update_menu/<int:pk>",views.update_menu,name="update_menu"),
    path("approve_menu/<int:pk>",views.approve_menu,name="approve_menu"),
    path("<int:pk>/",views.view_menu,name="view_menu"),
    path("make_menu_holiday/<int:pk>",views.make_menu_holiday,name="make_menu_holiday"),
    
    #weekly
    path("weekly_menu",views.weekly_menu,name="weekly_menu"),
    path("view_weekly_menu/<int:week>",views.view_weekly_menu,name="view_weekly_menu"),
    path("all_weekly_menus/",views.all_weekly_menus,name="all_weekly_menus"),
    path("<int:pk>/orders/",views.weekly_menu_all_orders,name="weekly_menu_all_orders"),
    # path("create_weekly_menu",views.create_weekly_menu,name="create_weekly_menu"),
    # path("update_weekly_menu",views.update_weekly_menu,name="update_weekly_menu"),
    # path("delete_weekly_menu",views.delete_weekly_menu,name="delete_weekly_menu"),
    
]