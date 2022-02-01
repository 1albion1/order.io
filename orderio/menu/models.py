from django.db import models
from meal.models import Meal
from django.utils import timezone
from django.urls import reverse
from datetime import date

# Create your models here.
class WeeklyMenu(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    week = models.IntegerField(default=int(timezone.now().isocalendar().week))
    year = models.IntegerField(default=int(timezone.now().isocalendar().year))
    
    def __str__(self):
        return f"{date.fromisocalendar(self.year,self.week,1).strftime('%d/%b/%y')}-{date.fromisocalendar(self.year,self.week,7).strftime('%d/%b/%y')}"
    
    class Meta:
        ordering = ('-year','-week',)
    
    def get_absolute_url(self):
        return reverse("menu:view_weekly_menu", kwargs={"week": self.week,"year":self.year})
    
    def get_total_order_count(self):
        total = 0
        for menu in self.menu_set.all():
            total += menu.order_set.all().count()
        return total
    

class Menu(models.Model):
    CAPACITY = 7
    
    Monday = 1
    Tuesday =2
    Wendnesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7
    
    DAYS = (
            (Monday,"Monday"),
            (Tuesday,"Tuesday"),
            (Wendnesday,"Wendnesday"),
            (Thursday,"Thursday"),
            (Friday,"Friday"),   
            (Saturday,"Saturday"), 
            (Sunday,"Sunday"),    
            )
    #relationships
    meals = models.ManyToManyField(Meal)
    weekly_menu = models.ForeignKey(WeeklyMenu,null=True,on_delete=models.CASCADE)
    #attributes
    created_at = models.DateTimeField(auto_now_add=True)
    avability = models.IntegerField(default=2)
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(blank=True,null=True)
    created_for = models.IntegerField(choices=DAYS,default=Monday,null=True,blank=True)
    
    
    class Meta:
        ordering = ('weekly_menu','created_for',)
    
    def __str__(self):
        
        try: 
            week = self.weekly_menu.week
            year = self.weekly_menu.year
        except:
            week = ""
            year = ""
        return str(date.fromisocalendar(year,week,self.created_for).strftime("%A, %d/%b/%y"))
    
    def allowes_orders(self):
        return (timezone.now()-self.approved_at)<timezone.timedelta(hours=self.avability)
    
    def get_order_total(self):
        return self.order_set.count()
    
    def get_menu_total_price(self):
        total = 0
        for meal in self.meals.all():
            total+=meal.price
        return total
    
    def get_day_name(self):
        name =""
        for day in Menu.DAYS:
            if day[0] == self.created_for:
                name = day[1]
                break
        return name
 

    def get_absolute_url(self):
        return reverse("menu:view_menu", kwargs={"pk": self.pk})