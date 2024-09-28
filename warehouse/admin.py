from django.contrib import admin
from .models import Phone, Brand, Country
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import messages
from celery import shared_task
import csv
from django.http import HttpResponse


@shared_task
def delete_phones_task(phone_ids):
    """
    A Celery task to delete selected phones.
    """
    Phone.objects.filter(id__in=phone_ids).delete()


@admin.action(description="Delete selected phones asynchronously")
def delete_phones(modeladmin, request, queryset):
    """
    Custom admin action to delete phones asynchronously using Celery.
    """
    phone_ids = list(queryset.values_list('id', flat=True))
    delete_phones_task.delay(phone_ids)
    modeladmin.message_user(request, "Deletion task has been submitted to Celery.", messages.SUCCESS)


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'country', 'price', 'inventory', 'status', 'color_display')
    list_filter = ('status', 'brand', 'country', 'color', 'price')
    search_fields = ('model', 'brand__name', 'country__name')
    actions = [delete_phones]
    ordering = ['brand', 'model']
    list_per_page = 20

    def color_display(self, obj):
        """
        A custom method to display color as a colored block in the list view.
        """
        return format_html(
            '<div style="background-color: {}; width: 20px; height: 20px;"></div>',
            obj.color.name if obj.color else 'transparent'
        )

    color_display.short_description = 'Color'

    def save_model(self, request, obj, form, change):
        """
        Custom save behavior to set default values.
        """
        if obj.inventory == 0:
            obj.status = 'unavailable'
        else:
            obj.status = 'available'
        super().save_model(request, obj, form, change)

    def export_as_csv(self, request, queryset):
        """
        Custom action to export selected records to CSV.
        """
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export selected phones as CSV"

    actions = [delete_phones, export_as_csv]

    fieldsets = (
        (None, {
            'fields': ('brand', 'model', 'country', 'display_size', 'price')
        }),
        ('Inventory & Status', {
            'fields': ('inventory', 'status', 'color')
        }),
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'total_phones')
    search_fields = ('name', 'country__name')
    ordering = ['name']

    def total_phones(self, obj):
        """
        A custom method to show the total number of phones under each brand.
        """
        return obj.phone_set.count()

    total_phones.short_description = 'Total Phones'


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_brands')
    search_fields = ('name',)

    def total_brands(self, obj):
        """
        A custom method to show the total number of brands in each country.
        """
        return obj.brands.count()

    total_brands.short_description = 'Total Brands'
