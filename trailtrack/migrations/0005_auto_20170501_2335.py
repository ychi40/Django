# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-01 13:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trailtrack', '0004_auto_20170429_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trailtrack',
            name='period',
            field=models.CharField(max_length=50),
        ),
    ]