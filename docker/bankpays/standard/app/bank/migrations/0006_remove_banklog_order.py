# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-20 08:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0005_auto_20170220_0759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banklog',
            name='order',
        ),
    ]
