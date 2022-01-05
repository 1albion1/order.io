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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Category Name*'})
        self.fields['description'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Category Description'})
    
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
            "name":"Meal Name*",
            "description":"Meal Description",
            "price" : "Meal Price*",
            "calories" : "Total Calories",
            "meal_img" : "Image"
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Meal Name*'})
        self.fields['description'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Meal Description'})
        self.fields['calories'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Meal Calories'})
        self.fields['price'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Meal Price*'})
        self.fields['meal_img'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Meal Image'})
        self.fields['category'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Meal Category*'})
    
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if self.instance.pk is None:
            if Meal.objects.filter(name=name):
                raise forms.ValidationError("This Meal name already exists!",code="Exists!")
        if len(name)>50:
            raise forms.ValidationError("The Meal name is too long. Maximum 50 characters!")
        return name
    
    def clean_price(self):
        price = self.cleaned_data.get("price")
        if float(price) <=0:          
            raise forms.ValidationError("The meal price is incorrect!",code="Incorrect!")
        return price
    
    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description)>2048:
            raise forms.ValidationError("The Meal description is too long. Maximum 1024 characters!")
        return description