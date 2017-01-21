# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-21 00:27
from __future__ import unicode_literals

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0038_auto_20170114_0418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(default='avatar/default.jpg', null=True, upload_to='avatar', verbose_name='\u5934\u50cf'),
        ),
    ]
