# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-23 18:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_cart_orderpizza_ordertopping'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 23, 18, 17, 27, 679530, tzinfo=utc), verbose_name='date created'),
        ),
    ]