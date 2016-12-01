# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 23:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('message', '0004_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='users',
            field=models.ManyToManyField(related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
