# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from faker import Factory

from service.consumer.models import Profile


def run():
    fakes = Factory.create('zh_CN')
    users = get_user_model().objects.filter(profile__isnull=True)

    for user in users:
        profile, status = Profile.objects.get_or_create(owner=user)

        if status:
            profile.nick = fakes.name()
            profile.save()
