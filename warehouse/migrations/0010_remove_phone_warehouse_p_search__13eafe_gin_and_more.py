# Generated by Django 4.2 on 2024-09-26 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0009_alter_phone_search_vector'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='phone',
            name='warehouse_p_search__13eafe_gin',
        ),
        migrations.RemoveField(
            model_name='phone',
            name='search_vector',
        ),
    ]
