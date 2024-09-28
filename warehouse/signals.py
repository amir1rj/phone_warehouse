from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Phone
from django.contrib.postgres.search import SearchVector,SearchQuery


@receiver(post_save, sender=Phone)
def update_search_vector(sender, instance, **kwargs):
    instance.search_vector = SearchVector('model'), SearchVector('brand__name')
