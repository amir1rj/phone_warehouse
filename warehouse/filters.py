import django_filters
from .models import Phone
class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class PhoneFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter(field_name='price', label="Price Range")
    inventory = django_filters.RangeFilter(field_name='inventory', label="Inventory Range")
    display_size = django_filters.RangeFilter(field_name='display_size', label="Display Size Range")
    color = CharInFilter(field_name='color__name', lookup_expr='in', label="Colors")
    country = CharInFilter(field_name='country__name', lookup_expr='in', label="Countries")
    brand_country = django_filters.CharFilter(field_name='brand__country__name', lookup_expr='icontains',
                                              label="Brand Country")
    brand = CharInFilter(field_name='brand__name', lookup_expr='in', label="Brands")

    status = django_filters.ChoiceFilter(field_name='status', choices=Phone.STATUS_CHOICES, label="Status")

    class Meta:
        model = Phone
        fields = ['price', 'inventory', 'display_size', 'color', 'country', 'brand', 'brand_country', 'status']
