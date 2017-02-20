# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from celery import shared_task

from .utils.jpush_audience import jpush_all, jpush_alias, jpush_extras


@shared_task
def send_verify_push(message, *args, **kwargs):
    status = jpush_alias(message, *args, **kwargs)
    return status


@shared_task
def send_verify_allpush(message):
    status = jpush_all(message)
    return status


@shared_task
def send_verify_extras(message, alias, extras):
    status = jpush_extras(message, alias, extras)
    return status
