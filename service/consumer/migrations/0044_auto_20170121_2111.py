# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-21 21:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0043_auto_20170121_2048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notice',
            options={'ordering': ('-pk',), 'verbose_name': '\u6d88\u606f\u4e2d\u5fc3', 'verbose_name_plural': '\u6d88\u606f\u4e2d\u5fc3'},
        ),
    ]
