# Generated by Django 4.1.9 on 2023-08-17 01:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
        ('inventories', '0002_remove_inventory_from_destination_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='customer',
            field=models.ForeignKey(limit_choices_to={'type': 'customer'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer', to='person.person'),
        ),
    ]
