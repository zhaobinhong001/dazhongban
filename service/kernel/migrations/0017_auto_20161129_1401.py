# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kernel', '0016_auto_20161129_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumption',
            name='date',
            field=models.DateField(auto_now_add=True, max_length=11, verbose_name='\u6d88\u8d39\u65f6\u95f4'),
        ),
    ]
