from django.urls import path
from . import views
app_name = "manager"
urlpatterns = [
    
    path("",views.index, name="index"),
    #reports
    path("reports",views.reports_index,name="reports_index"),
    path("user_spendings",views.user_spendings,name="user_spendings"),
    path("total_orders_by_department",views.total_orders_by_department,name="total_orders_by_department"),
    #chart links
    path("population_chart/<int:pk>",views.population_chart,name='population_chart'),
    path("chart_total_orders_by_department/<int:pk>",views.chart_total_orders_by_department,name="chart_total_orders_by_department"),
    path("number_of_orders_by_day",views.number_of_orders_by_day,name="number_of_orders_by_day")
]
