# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-28 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trailtrack', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trailtrack',
            name='latitude',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='trailtrack',
            name='longitude',
            field=models.CharField(max_length=50),
        ),
    ]
