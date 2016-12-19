# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-19 02:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0006_auto_20161219_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='receiver',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract_receiver', to=settings.AUTH_USER_MODEL),
        ),
    ]
