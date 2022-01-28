from django.urls import path
from . import views
app_name = "order"
urlpatterns = [
    path("daily_orders",views.daily_orders,name="daily_orders"),
    path("create_order",views.create_order,name="create_order"),
    path("<int:pk>",views.view_order,name="view_order"),
    path("user_order_history",views.user_order_history,name="user_order_history"),
    path("delete_order/<int:pk>",views.delete_order,name="delete_order"),
    path("change_order_status/<int:pk>/<int:status>",views.change_order_status,name="change_order_status"),
    path("add_to_order",views.add_to_order,name="add_to_order"),
    path("all_orders_this_week",views.all_orders_this_week,name="all_orders_this_week"),
    path("full_order_history",views.full_order_history,name="full_order_history"),
    path("custom_order/",views.custom_order,name="custom_order")
]
