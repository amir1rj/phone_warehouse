from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector, SearchQueryField
from django.db import models



class Phone(models.Model):
    STATUS_CHOICES = (
        ('available', 'موجود'),
        ('unavailable', 'نا موجود'),
    )
    brand = models.ForeignKey(
        'Brand', on_delete=models.SET_NULL, null=True,
        related_name='phone_set', verbose_name="برند"
    )
    model = models.CharField(max_length=50, unique=True, verbose_name="مدل")
    country = models.ForeignKey(
        'Country', on_delete=models.SET_NULL, null=True,
        related_name='phone_set', verbose_name="کشور"
    )
    display_size = models.FloatField(verbose_name="اندازه نمایشگر")
    price = models.PositiveIntegerField(verbose_name="قیمت")
    color = models.ForeignKey(
        'Color', on_delete=models.SET_NULL, null=True,
        verbose_name="رنگ"
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100, verbose_name="وضعیت"
    )
    inventory = models.IntegerField(default=0, verbose_name="موجودی")
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        verbose_name = "تلفن"
        verbose_name_plural = "تلفن‌ها"
        indexes = [
            GinIndex(fields=['search_vector']),
        ]

    def __str__(self):
        return f'{self.brand} {self.model} {self.price}'

    def save(self, *args, **kwargs):
        # Automatically set status to 'unavailable' if inventory is 0 or less
        if self.inventory <= 0:
            self.status = 'unavailable'
        else:
            self.status = 'available'
        self.search_vector = self.model + " " + self.brand.name

        super().save(*args, **kwargs)


class Brand(models.Model):
    country = models.ForeignKey(
        'Country', on_delete=models.SET_NULL, null=True,
        related_name='brands', verbose_name="کشور"
    )
    name = models.CharField(max_length=100, verbose_name="نام برند")

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برندها"

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام کشور", unique=True)

    class Meta:
        verbose_name = "کشور"
        verbose_name_plural = "کشورها"

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام رنگ", unique=True)

    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ‌ها"

    def __str__(self):
        return self.name
