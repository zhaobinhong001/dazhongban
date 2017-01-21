# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import exceptions
from rest_framework.compat import set_rollback
from rest_framework.response import Response

errors = {
    'PermissionDenied': '',
    'SYSTEM_ERROR': '',
}


def get_exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, exceptions.APIException):
        headers = {}

        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header

        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, dict):
            if exc.detail.get('card'):
                data = {'detail': '卡号已存在'}
            else:
                data = [v[0] for k, v in exc.detail.items()]
                data = {'detail': ','.join(data)}
                print data
        elif isinstance(exc.detail, list):
            data = {'detail': ''.join(exc.detail)}
        else:
            data = {'detail': exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    # elif isinstance(exc, Http404):
    #     msg = _('Not found.')
    #     data = {'msgs': six.text_type(msg)}
    #
    #     set_rollback()
    #     return Response(data, status=status.HTTP_404_NOT_FOUND)

    # elif isinstance(exc, PermissionDenied):
    #     msg = _('Permission denied.')
    #     data = {'msgs': six.text_type(msg)}
    #
    #     set_rollback()
    #     return Response(data, status=status.HTTP_403_FORBIDDEN)

    # Note: Unhandled exceptions will raise a 500 error.
    return None


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    response = get_exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    # if response:
    #     if response.data.get('detail'):
    #         data = None
    #         detail = response.data.get('detail')
    #
    #         del response.data['detail']
    #
    #         if isinstance(detail, ReturnDict):
    #             data = [v[0] for k, v in detail.items()]
    #             msgs = {}
    #
    #             # for k, v in detail.items():
    #             #     msgs[k] = k + v[0]
    #             #     msgs[k] = v[0]
    #         else:
    #             msgs = detail
    #
    #         if data:
    #             msgs = str(data[0])
    #
    #         response.data['detail'] = msgs
    # else:
    #     print exc, 'exc'

    return response
