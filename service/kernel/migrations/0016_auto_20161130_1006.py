# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kernel', '0015_auto_20161129_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relancement',
            name='creation_time',
            field=models.DateField(auto_now_add=True, verbose_name='\u7533\u8bf7\u65f6\u95f4'),
        ),
    ]
