from django.urls import path
from . import views
app_name = "manager"
urlpatterns = [
    
    path("",views.index, name="index"),
    #reports
    path("reports",views.reports_index,name="reports_index"),
    path("user_spendings",views.user_spendings,name="user_spendings"),
    path("total_orders_by_department",views.total_orders_by_department,name="total_orders_by_department"),
    path("most_ordered_meals",views.most_ordered_meals,name="most_ordered_meals"),
    path("most_ordered_category",views.most_ordered_category,name="most_ordered_category"),
    
    #chart links
    path("chart_user_spendings/<int:pk>",views.chart_user_spendings,name='chart_user_spendings'),
    path("chart_total_orders_by_department/<int:pk>",views.chart_total_orders_by_department,name="chart_total_orders_by_department"),
    path("number_of_orders_by_day",views.number_of_orders_by_day,name="number_of_orders_by_day"),
    path("chart_most_ordered_meals/<int:pk>",views.chart_most_ordered_meals,name="chart_most_ordered_meals"),
    path("chart_most_ordered_category",views.chart_most_ordered_category,name="chart_most_ordered_category"),
]
