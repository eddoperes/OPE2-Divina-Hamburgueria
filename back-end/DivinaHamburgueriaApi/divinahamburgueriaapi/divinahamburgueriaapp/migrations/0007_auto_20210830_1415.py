# Generated by Django 3.2.6 on 2021-08-30 17:15

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('divinahamburgueriaapp', '0006_auto_20210828_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('cpf', models.CharField(max_length=11)),
            ],
            options={
                'db_table': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(max_length=8)),
                ('logradouro', models.CharField(max_length=100)),
                ('numero', models.IntegerField()),
                ('complemento', models.CharField(max_length=50)),
                ('bairro', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
                ('uf', models.CharField(max_length=2)),
            ],
            options={
                'db_table': 'endereco',
            },
        ),
        migrations.CreateModel(
            name='Telefone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ddd', models.CharField(max_length=2)),
                ('numero', models.CharField(max_length=9)),
            ],
            options={
                'db_table': 'telefone',
            },
        ),
        migrations.AlterField(
            model_name='cardapio',
            name='dataativado',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 30, 17, 15, 30, 341467, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cardapio',
            name='datacriado',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 30, 17, 15, 30, 341467, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cardapioitemdocardapio',
            name='dataativado',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 30, 17, 15, 30, 343466, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cardapioitemdocardapio',
            name='datacriado',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 30, 17, 15, 30, 343466, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='dataativado',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 30, 17, 15, 30, 340468, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='datacriado',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 30, 17, 15, 30, 340468, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='PedidoSalao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.IntegerField(default=1)),
                ('dataemitido', models.DateTimeField(default=datetime.datetime(2021, 8, 30, 17, 15, 30, 366463, tzinfo=utc))),
                ('datacancelado', models.DateTimeField(null=True)),
                ('dataentregue', models.DateTimeField(null=True)),
                ('observacao', models.CharField(max_length=400)),
                ('cliente', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='clientes', to='divinahamburgueriaapp.cliente')),
                ('usuario', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='usuarios', to='divinahamburgueriaapp.usuario')),
            ],
            options={
                'db_table': 'pedidosalao',
            },
        ),
        migrations.AddField(
            model_name='cliente',
            name='endereco',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='enderecos', to='divinahamburgueriaapp.endereco'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='telefone',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='telefones', to='divinahamburgueriaapp.telefone'),
        ),
    ]
