# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-19 02:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0005_auto_20161219_0230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='type',
            field=models.CharField(choices=[('0', '\u626b\u7801\u652f\u4ed8'), ('1', '\u7b2c\u4e09\u65b9\u652f\u4ed8')], default=0, max_length=100, verbose_name='\u6d88\u8d39\u7c7b\u578b'),
        ),
    ]
