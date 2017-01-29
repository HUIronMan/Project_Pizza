# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-25 15:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_cart_created_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('state', models.SmallIntegerField(default=0)),
                ('from_cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='orders.Cart')),
                ('customer_name', models.CharField(max_length=255)),
                ('customer_address', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='cart',
            name='created_on',
        ),
    ]