# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from service.kernel.utils.sms import send_sms
from celery import shared_task


@shared_task
def send_verify_code(mobile, message):
    status = send_sms(mobile, message)
    return status
