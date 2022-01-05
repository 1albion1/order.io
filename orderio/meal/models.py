from django.db import models
from django.urls import reverse
from main.images_rename import img_path
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("meal:view_category", kwargs={"pk": self.pk})
    
    
class Meal(models.Model):
    #realtionships    
    category =models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    #attributes
    name = models.CharField(max_length=100,blank=True)
    price = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    description = models.TextField(blank=True,null=True)
    calories = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    meal_img = models.ImageField(null=True,default="meal-default.png",upload_to=img_path)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("meal:view_meal", kwargs={"pk": self.pk})

