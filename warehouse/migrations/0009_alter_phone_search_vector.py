# Generated by Django 4.2 on 2024-09-26 09:17

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0008_phone_search_vector_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(blank=True, null=True),
        ),
    ]
