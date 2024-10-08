# Generated by Django 4.2 on 2024-09-26 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_alter_phone_model_delete_phonemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brands', to='warehouse.country'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='phone_set', to='warehouse.brand'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='phone_set', to='warehouse.country'),
        ),
    ]
