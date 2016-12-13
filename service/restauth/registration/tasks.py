# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from service.kernel.utils.jpush_audience import jpush_push, jpush_all
from service.kernel.utils.sms import send_sms
from celery import shared_task


@shared_task
def send_verify_code(mobile, message):
    status = send_sms(mobile, message)
    return status


def send_verify_push(message, alias):
    status = jpush_push(message, alias)
    return status


def send_verify_allpush(message):
    status = jpush_all(message)
    return status
