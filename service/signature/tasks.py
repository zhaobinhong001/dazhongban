# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import requests
from celery import shared_task
from django.conf import settings

from service.signature.models import Identity


@shared_task
def query_sign(dn, *args, **kwargs):
    result = requests.post(settings.VERIFY_GATEWAY + '/Query', data=dn)
    result = result.json()

    if result.get('status') == '3':
        identity = Identity.objects.get(dn=dn)

        if identity:
            identity.serial = result.get('serialNo')

            if result.get('endDate'):
                identity.enddate = result.get('endDate')

            identity.save()

    return result
