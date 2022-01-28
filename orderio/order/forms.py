from django.forms import ModelForm
from .models import Order

class OrderCreationForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs.update({'class': 'form-control form-control-user','required':""})
        self.fields['meals'].widget.attrs.update({'class': 'form-control form-control-user','required':""})
        self.fields['menu'].widget.attrs.update({'class': 'form-control form-control-user','required':""})
        self.fields['order_status'].widget.attrs.update({'class': 'form-control form-control-user'})
        self.fields['order_cost'].widget.attrs.update({'class': 'form-control form-control-user'})