# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-23 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0100_auto_20170118_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='real_estate_raw',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='address',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
