# Generated by Django 3.2.6 on 2021-10-15 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divinahamburgueriaapp', '0027_auto_20211015_0819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemdoestoque',
            name='descricao',
        ),
        migrations.AddField(
            model_name='itemdoestoque',
            name='tipo',
            field=models.IntegerField(default=1),
        ),
    ]
