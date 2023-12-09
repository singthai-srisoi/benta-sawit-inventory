# Generated by Django 4.1.9 on 2023-12-09 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0004_inventory_supplier_qty'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='bucket',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inventory',
            name='customer_ticket_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='factory_nett',
            field=models.IntegerField(default=0),
        ),
    ]