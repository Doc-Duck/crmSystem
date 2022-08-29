from django import forms
from django.forms import Textarea, TextInput, Select
from .models import *


class OrderByForm(forms.Form):
    choices = (('manager__first_name', 'name'), ('-total', 'sales'))
    order_by = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'class': 'form-select col me-2 ms-2'}))


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'content']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Title', 'style': 'height: 20%'}),
            'content': TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Content', 'style': 'height: 20%'})
        }


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Managers
        fields = ['first_name', 'last_name', 'department', 'city', 'region', 'email', 'address']
        widgets = {
            'first_name': TextInput(attrs={'type': "text", 'class': "form-control", 'placeholder': "first name"}),
            'last_name': TextInput(attrs={'type': "text", 'class': "form-control", 'placeholder': "last name"}),
            'department': Select(attrs={'type': "text", 'class': "form-select", 'placeholder': "department"}),
            'city': TextInput(attrs={'type': "text", 'class': "form-control", 'placeholder': "city"}),
            'region': TextInput(attrs={'type': "text", 'class': "form-control", 'placeholder': "region"}),
            'email': TextInput(attrs={'type': "text", 'class': "form-control", 'placeholder': "email"}),
            'address': TextInput(attrs={'type': "text", 'class': "form-control", 'placeholder': "address"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'type': "text", 'class': "form-control", 'placeholder': "Product name"}),
            'price': TextInput(attrs={'type': "number", 'class': "form-control", 'placeholder': "Price"}),
            'department': Select(attrs={'type': "text", 'class': "form-select", 'placeholder': "department"})
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = '__all__'
        widgets = {
            'first_name': TextInput(attrs={'type': "text", 'class': "form-control", 'placeholder': "Client First name"}),
            'last_name': TextInput(attrs={'type': "text", 'class': "form-control", 'placeholder': "Client Last name"}),
            'email': TextInput(attrs={'type': "text", 'class': "form-control", 'placeholder': "Client`s email"}),
        }


class Sales_add(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['client']
        widgets = {
            'client': Select(attrs={'type': "text", 'class': "form-select", 'placeholder': "Client name"}),
        }


class ProductSale(forms.ModelForm):
    class Meta:
        model = Products_sale
        fields = ['products', 'quantity']
        widgets = {
            'products': Select(attrs={'type': "text", 'class': "form-select pr-form", 'placeholder': "Products"}),
            'quantity': TextInput(attrs={'type': "number", 'class': "form-control mb-2", 'placeholder': "Quantity"}),
        }