# Generated by Django 3.2.6 on 2021-10-11 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divinahamburgueriaapp', '0025_pedidodecompra_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidodecompraitemdoestoque',
            name='estocado',
            field=models.BooleanField(default=False),
        ),
    ]
