# Generated by Django 4.2 on 2024-09-26 09:12

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0007_alter_country_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddIndex(
            model_name='phone',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='warehouse_p_search__13eafe_gin'),
        ),
    ]
