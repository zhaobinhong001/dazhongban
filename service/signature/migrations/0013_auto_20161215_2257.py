# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-15 22:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signature', '0012_auto_20161214_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identity',
            name='expired',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='\u6709\u6548\u671f'),
        ),
    ]
