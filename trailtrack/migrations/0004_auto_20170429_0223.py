# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-28 16:23
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('trailtrack', '0003_auto_20170429_0157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trailtrack',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='trailtrack',
            name='longitude',
        ),
        migrations.AddField(
            model_name='trailtrack',
            name='geocode',
            field=jsonfield.fields.JSONField(default=(33, 145)),
            preserve_default=False,
        ),
    ]