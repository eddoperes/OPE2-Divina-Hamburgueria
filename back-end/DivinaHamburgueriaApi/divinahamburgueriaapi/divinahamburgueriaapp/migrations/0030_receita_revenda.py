# Generated by Django 3.2.6 on 2021-10-16 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('divinahamburgueriaapp', '0029_auto_20211015_1232'),
    ]

    operations = [
        migrations.CreateModel(
            name='Revenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemdocardapio', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='itensdocardapiorevenda', to='divinahamburgueriaapp.itemdocardapio')),
                ('itemdoestoque', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='itensdoestoquerevenda', to='divinahamburgueriaapp.itemdoestoque')),
            ],
            options={
                'db_table': 'revenda',
            },
        ),
        migrations.CreateModel(
            name='Receita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('quantidade', models.IntegerField(default=1)),
                ('unidade', models.CharField(default='', max_length=10)),
                ('itemdocardapio', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='itensdocardapioreceita', to='divinahamburgueriaapp.itemdocardapio')),
            ],
            options={
                'db_table': 'receita',
            },
        ),
    ]
