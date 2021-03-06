# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 10:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='MenuPizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MenuSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('price', models.IntegerField(default=0)),
                ('ntopings', models.IntegerField(default=3)),
            ],
        ),
        migrations.CreateModel(
            name='MenuTopping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.SmallIntegerField(default=0)),
                ('customer_name', models.CharField(max_length=255)),
                ('customer_address', models.CharField(max_length=255)),
                ('from_cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.Cart')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Cart')),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pizza', to='orders.MenuPizza')),
                ('pizza_half', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pizza_half', to='orders.MenuPizza')),
            ],
        ),
        migrations.CreateModel(
            name='OrderSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.OrderPizza')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.MenuSize')),
            ],
        ),
        migrations.CreateModel(
            name='OrderTopping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.OrderPizza')),
                ('topping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.MenuTopping')),
            ],
        ),
    ]
