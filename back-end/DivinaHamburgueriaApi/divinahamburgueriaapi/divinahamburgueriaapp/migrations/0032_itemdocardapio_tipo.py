# Generated by Django 3.2.6 on 2021-10-18 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divinahamburgueriaapp', '0031_auto_20211016_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemdocardapio',
            name='tipo',
            field=models.IntegerField(default=1),
        ),
    ]
