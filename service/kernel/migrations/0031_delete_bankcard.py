# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-23 01:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kernel', '0030_auto_20161223_0019'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BankCard',
        ),
    ]
