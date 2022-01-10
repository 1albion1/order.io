from django.db import models
from account.models import CustomUser
from main.images_rename import img_path
from django.urls import reverse
# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=20,blank=True)

    def __str__(self):
        return self.name
class Employee(models.Model):
    #relationships
    user = models.OneToOneField(CustomUser,null=True,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    daily_allowance = models.DecimalField(max_digits=6,decimal_places=2,default=5)
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    profile_pic = models.ImageField(null=True,default="default.png",upload_to=img_path)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse("employee:employee_profile", kwargs={"pk": self.user.pk})
    
