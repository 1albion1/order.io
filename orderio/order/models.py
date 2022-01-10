from django.db import models
from employee.models import Employee
from meal.models import Meal
from menu.models import Menu
from django.urls import reverse
# Create your models here.

class Order(models.Model):
    STATUS = (
        ("Pending","Pending"),
        ("Accepted","Accepted"),
        ("Denied","Denied")
        )
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
    meals = models.ManyToManyField(Meal,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    menu = models.ForeignKey(Menu,blank=True,on_delete=models.CASCADE,null=True,)
    order_status = models.CharField(default="Pending",choices=STATUS,blank=True,null=True,max_length=10)
    order_cost = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    
    class Meta:
        ordering = ("-created_at",)
        
    def get_created_at_date(self):
        return self.created_at.date()
    
    def __str__(self):
        return f"{str(self.created_at.date())} {self.employee.user.username}"
    
    def get_absolute_url(self):
        return reverse("order:view_order", kwargs={"pk": self.pk})
    
    
