from django import forms
from .models import Phone, Brand, Color, Country
from django.core.exceptions import ValidationError
import re


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['brand', 'model', 'country', 'display_size', 'price', 'color', 'inventory']
        labels = {
            'brand': 'برند',
            'model': 'مدل',
            'country': 'کشور',
            'display_size': 'صفحه نمایش(اینچ)',
            'price': 'قیمت(تومان)',
            'color': 'رنگ',
            'inventory': 'موجودی',
        }

    def __init__(self, *args, **kwargs):
        super(PhoneForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_model(self):
        model = self.cleaned_data.get('model')
        if not re.match(r'^[a-zA-Z0-9\s]+$', model):
            raise ValidationError('Model name should contain only letters and numbers.')
        return model

    def clean_display_size(self):
        display_size = self.cleaned_data.get('display_size')
        if not (3.0 <= display_size <= 10.0):
            raise ValidationError('Display size must be between 3.0 and 10.0 inches.')
        return display_size

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('Price must be a positive number.')
        if price > 1000000:
            raise ValidationError('Price seems too high.')
        return price

    def clean_inventory(self):
        inventory = self.cleaned_data.get('inventory')
        if inventory < 0:
            raise ValidationError('Inventory cannot be negative.')
        return inventory


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ['name']
        labels = {
            'name': 'Color Name',
        }

    def __init__(self, *args, **kwargs):
        super(ColorForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise ValidationError('Color name should only contain alphabetic characters.')
        return name


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'country']
        labels = {
            'name': 'Brand Name',
            'country': 'Country of Origin',
        }

    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise ValidationError('Brand name should only contain alphabetic characters.')
        return name


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']
        labels = {
            'name': 'Country Name',
        }

    def __init__(self, *args, **kwargs):
        super(CountryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise ValidationError('Country name should only contain alphabetic characters.')
        return name
