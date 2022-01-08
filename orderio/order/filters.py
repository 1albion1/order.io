import  django_filters
from .models import Order

class OrderFilter(django_filters.FilterSet):
    Monday = 1
    Tuesday =2
    Wendnesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7
    CHOICES = ((Monday,"Monday"),
            (Tuesday,"Tuesday"),
            (Wendnesday,"Wendnesday"),
            (Thursday,"Thursday"),
            (Friday,"Friday"),   
            (Saturday,"Saturday"), 
            (Sunday,"Sunday"),    
            )
    day = django_filters.ChoiceFilter(choices=CHOICES,method="get_by_day")
    
    class Meta:
        model = Order
        fields = ["employee","order_status","menu"]
    
    def get_by_day(self,queryset,name,value):
        return queryset.filter(menu__created_for = value)
 
        