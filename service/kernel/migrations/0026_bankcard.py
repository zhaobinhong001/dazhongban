# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-14 20:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kernel', '0025_delete_bankcard'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardis_bank', models.CharField(max_length=100, verbose_name='\u53d1\u5361\u884c\u540d\u79f0')),
                ('card_name', models.CharField(max_length=100, verbose_name='\u5361\u540d\u79f0')),
                ('num_name', models.CharField(max_length=100, verbose_name='\u4e3b\u8d26\u53f7')),
                ('card_type', models.CharField(max_length=100, verbose_name='\u5361\u79cd')),
            ],
            options={
                'verbose_name': '\u94f6\u884c\u5361\u5361\u8868',
                'verbose_name_plural': '\u94f6\u884c\u5361\u5361\u8868',
            },
        ),
    ]
