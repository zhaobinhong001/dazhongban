# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-06 01:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0028_auto_20170306_0052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transfer',
            name='account',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='bank_accountName',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='consumer',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='receipt',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='signaid',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='title',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='type',
        ),
    ]
