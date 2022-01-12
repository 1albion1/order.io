from django.urls import path
from . import views
app_name = "meal"
urlpatterns = [
    path("create_meal",views.create_meal,name="create_meal"),
    path("update_meal/<int:pk>",views.update_meal,name="update_meal"),
    path("delete_meal/<int:pk>",views.delete_meal,name="delete_meal"),
    path("<int:pk>",views.view_meal,name="view_meal"),
    path("all_meals",views.all_meals,name="all_meals"),
    
    path("create_category",views.create_category,name="create_category"),
    path("update_category/<int:pk>",views.update_category,name="update_category"),
    path("delete_category/<int:pk>",views.delete_category,name="delete_category"),
    path("category/<int:pk>",views.view_category,name="view_category"),
    path("all_categories",views.all_categories,name="all_categories"),
]