# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-17 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0097_property_online'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realestate',
            name='desc',
            field=models.TextField(blank=True, null=True),
        ),
    ]
