from django.db import models
from account.models import CustomUser
# Create your models here.

class Notification(models.Model):
    TYPES = (
        (0,"danger"),
        (1,"success"),
        (2,'warning'),
        (3,'info')
    )
    to_user = models.ForeignKey(CustomUser,null=True,blank=True,on_delete=models.CASCADE,related_name="notification_to")
    from_user = models.ForeignKey(CustomUser,null=True,blank=True,on_delete=models.CASCADE,related_name="notification_from")
    text = models.CharField(blank=True,null=True,max_length=1024)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(blank=True,null=True,choices=TYPES,default=3)
    
    class Meta:
        ordering = ['-date']
    
    def get_type(self):
        name =""
        for type in Notification.TYPES:
            if type[0] == self.type:
                name = type[1]
                break
        return name