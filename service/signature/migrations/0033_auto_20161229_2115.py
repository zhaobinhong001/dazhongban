# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signature', '0032_auto_20161229_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identity',
            name='dn',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='DN'),
        ),
    ]
