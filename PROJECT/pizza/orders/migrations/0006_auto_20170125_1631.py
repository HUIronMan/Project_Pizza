# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-25 16:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20170125_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='from_cart',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.Cart'),
        ),
    ]