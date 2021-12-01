# Generated by Django 3.2.6 on 2021-10-16 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('divinahamburgueriaapp', '0030_receita_revenda'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemdocardapio',
            name='receita',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receitas', to='divinahamburgueriaapp.receita'),
        ),
        migrations.AddField(
            model_name='itemdocardapio',
            name='revenda',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='revendas', to='divinahamburgueriaapp.revenda'),
        ),
    ]
