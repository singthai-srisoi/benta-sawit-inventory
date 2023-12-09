# Generated by Django 4.1.9 on 2023-08-16 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0001_initial'),
        ('person', '0001_initial'),
        ('inventories', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='from_destination',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='to_destination',
        ),
        migrations.AddField(
            model_name='inventory',
            name='destination',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='destinations.destination'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='supplier',
            field=models.ForeignKey(limit_choices_to={'type': 'supplier'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supplier', to='person.person'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='driver',
            field=models.ForeignKey(limit_choices_to={'type': 'driver'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='driver', to='person.person'),
        ),
    ]