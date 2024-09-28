from rest_framework import serializers
from .models import Phone


class PhoneListSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    country_name = serializers.CharField(source='country.name', read_only=True)
    color_name = serializers.CharField(source='color.name', read_only=True)
    brand_country_name = serializers.CharField(source='brand.country.name', read_only=True)

    class Meta:
        model = Phone
        fields = ['model', 'display_size', 'price', 'inventory', 'brand_name', 'country_name', 'color_name',
                  'brand_country_name', 'status']
