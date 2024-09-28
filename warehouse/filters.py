import django_filters
from .models import Phone


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    """Custom filter to allow filtering by a list of character values."""
    pass


class PhoneFilter(django_filters.FilterSet):
    """Filter set for the Phone model to enable various filtering options."""
    price = django_filters.RangeFilter(field_name='price', label="Price Range")
    inventory = django_filters.RangeFilter(field_name='inventory', label="Inventory Range")
    display_size = django_filters.RangeFilter(field_name='display_size', label="Display Size Range")
    # Custom filter for color, allowing filtering by a list of color names.
    color = CharInFilter(field_name='color__name', lookup_expr='in', label="Colors")
    # Custom filter for country, allowing filtering by a list of country names.
    country = CharInFilter(field_name='country__name', lookup_expr='in', label="Countries")
    # Filter for brand country, allowing case-insensitive filtering by the name of the brand's country.
    brand_country = django_filters.CharFilter(field_name='brand__country__name', lookup_expr='icontains',
                                              label="Brand Country")
    # Custom filter for brand, allowing filtering by a list of brand names.
    brand = CharInFilter(field_name='brand__name', lookup_expr='in', label="Brands")

    status = django_filters.ChoiceFilter(field_name='status', choices=Phone.STATUS_CHOICES, label="Status")

    class Meta:
        model = Phone
        fields = ['price', 'inventory', 'display_size', 'color', 'country', 'brand', 'brand_country', 'status']
