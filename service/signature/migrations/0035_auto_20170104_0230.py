# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-04 02:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signature', '0034_auto_20170104_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identity',
            name='dn',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='DN'),
        ),
    ]
