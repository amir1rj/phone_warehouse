# Generated by Django 4.2 on 2024-09-26 11:22

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0014_alter_phone_search_vector'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='search_query',
            field=django.contrib.postgres.search.SearchQueryField(null=True),
        ),
    ]
