# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-23 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0101_auto_20170123_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='title',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='slug',
            field=models.SlugField(max_length=500, unique=True),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='telephone',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]