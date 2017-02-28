# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 21:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeatherRangerProject', '0002_auto_20170226_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperaturerange',
            name='is_in_five_day_range',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='temperaturerange',
            name='is_in_range',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='temperaturerange',
            name='is_in_sixteen_day_range',
            field=models.NullBooleanField(),
        ),
    ]
