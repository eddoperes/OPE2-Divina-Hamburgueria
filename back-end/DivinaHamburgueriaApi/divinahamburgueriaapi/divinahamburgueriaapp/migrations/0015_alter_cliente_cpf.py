# Generated by Django 3.2.6 on 2021-09-28 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divinahamburgueriaapp', '0014_auto_20210923_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cpf',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
