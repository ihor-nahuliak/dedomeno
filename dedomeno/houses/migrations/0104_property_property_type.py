# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-26 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0103_property_address_province'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='property_type',
            field=models.CharField(blank=True, choices=[('house', 'house'), ('room', 'room'), ('office', 'office'), ('garage', 'garage'), ('land', 'land'), ('commercial', 'commercial')], max_length=200, null=True),
        ),
    ]
