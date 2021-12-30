from django.contrib.auth import forms
from django.forms import ModelForm,CharField,DecimalField
from .models import Category,Meal
from django.core.validators import RegexValidator

class CategoryForm(ModelForm):
    name = CharField(required=True)
    class Meta():
        
        model = Category
        fields = ('name','description')
        exclude = []
        labels = {
            "name":"Enter Category Name",
            "description":"Enter description",
        }
    
    
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if self.instance.pk is None:
            if Category.objects.filter(name=name):
                raise forms.ValidationError("This category name already exists!",code="Exists!")
        if len(name)>50:
            raise forms.ValidationError("The Category name is too long. Maximum 50 characters!")
        return name
    
    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description)>1024:
            raise forms.ValidationError("The Category description is too long. Maximum 1024 characters!")
        return description
    
class MealForm(ModelForm):
    name = CharField(required=True)
    price = DecimalField(required=True)
    class Meta():
        model = Meal
        fields = "__all__"
        exclude = []
        labels = {
            "name":"Meal Name",
            "description":"Meal Description",
            "price" : "Meal Price",
            "calories" : "Total Calories",
            "meal_img" : "Image"
        }
    