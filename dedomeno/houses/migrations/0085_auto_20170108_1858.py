# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-08 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0084_room'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='looking_for',
            new_name='house_type',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='working',
            new_name='looking_for_student',
        ),
        migrations.AddField(
            model_name='property',
            name='name',
            field=models.CharField(blank=True, max_length=130, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='looking_for_gender',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='looking_for_worker',
            field=models.NullBooleanField(),
        ),
    ]
