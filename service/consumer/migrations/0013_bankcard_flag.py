# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0012_auto_20161129_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankcard',
            name='flag',
            field=models.CharField(choices=[('\u6536', '\u6536')], default='', max_length=10, verbose_name='\u5361\u7247\u7c7b\u578b'),
        ),
    ]