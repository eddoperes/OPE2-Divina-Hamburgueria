# Generated by Django 3.2.6 on 2021-09-28 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divinahamburgueriaapp', '0017_alter_pedidodelivery_observacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidodeliveryitemdocardapio',
            name='observacao',
            field=models.CharField(max_length=400, null=True),
        ),
    ]
