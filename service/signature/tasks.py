# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import requests
from celery import shared_task
from django.conf import settings

from service.kernel.utils.bank_random import bankcard
from service.signature.models import Identity
from service.consumer.models import Bankcard


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

            # 创建时，生成模拟银行卡号
            # identity.owner.bankcard_set.filter(bank=u'收付宝').delete()
            vcard, _ = Bankcard.objects.get_or_create(owner=identity.owner, bank=u'收付宝')
            vcard.card = bankcard()
            vcard.type = u'借记卡'
            vcard.save()

            # 更新用户等级
            identity.owner.level = identity.level
            identity.owner.credit = '50'
            identity.owner.save()

            # 更新真实姓名
            identity.owner.profile.name = identity.name
            identity.owner.profile.save()

    return result
