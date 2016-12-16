# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from service.kernel.utils.jpush_audience import jpush_push, jpush_all


@shared_task
def send_verify_push(message, alias):
    status = jpush_push(message, alias)
    return status


@shared_task
def send_verify_allpush(message):
    status = jpush_all(message)
    return status
