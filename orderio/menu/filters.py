import django_filters
from .models import Menu

class MenuFilter(django_filters.FilterSet):
    class Meta:
        model = Menu
        fields = "__all__"
    
    