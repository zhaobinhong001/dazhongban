# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import arrow
import requests
from celery import shared_task
from django.conf import settings

from service.consumer.models import Bankcard
from service.kernel.utils.bank_random import bankcard
from service.signature.models import Identity


def query_sign(dn, *args, **kwargs):
    owner = kwargs.get('owner', None)

    try:
        queryset = Identity.objects.filter(dn=dn)

        if owner:
            queryset = queryset.filter(owner=owner)

        identity = queryset.get()
    except Identity.DoesNotExist:
        return 'Identity.DoesNotExist'

    result = requests.post(settings.VERIFY_GATEWAY + '/Query', data=dn)
    result = result.json()

    identity.serial = result.get('serialNo')

    if result.get('endDate'):
        identity.enddate = arrow.get(result.get('endDate')).format('YYYY-MM-DD')

    print identity.enddate

    identity.save()

    # 创建时，生成模拟银行卡号
    nums = Bankcard.objects.filter(owner=identity.owner, bank=u'收付宝').count()

    if nums == 0:
        vcard = Bankcard()
        vcard.owner = identity.owner
        vcard.bank = u'收付宝'
        vcard.card = bankcard()
        vcard.type = u'虚拟卡'
        vcard.suffix = vcard.card[-4:]
        vcard.save()

    try:
        bcard = requests.get(url='%s/%s' % (settings.BANK_CARD, identity.cardNo))
        bcard = bcard.json()
        bcard = bcard.get('result')

        scard = Bankcard(owner=identity.owner, card=identity.cardNo)
        scard.bank = bcard.get('bank')
        scard.type = bcard.get('type')

        scard.suffix = identity.cardNo[-4:]
        scard.save()
    except Exception:
        pass

    # 更新用户等级
    identity.owner.level = identity.level
    identity.owner.credit = '50'
    identity.owner.save()

    # 更新真实姓名 'male', '男'), ('female', '女'))
    identity.owner.profile.name = identity.name
    identity.owner.profile.gender = 'male' if (int(identity.certId[-2:-1]) % 2) == 1 else 'female'
    identity.owner.profile.save()

    return result


@shared_task
def query_sign_task(dn, *args, **kwargs):
    return query_sign(dn, *args, **kwargs)
