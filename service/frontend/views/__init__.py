# -*- coding: utf-8 -*-

from .mobile import *
from .htdocs import *

def oauth(method):
    @functools.wraps(method)
    def warpper(*args, **kwargs):
        code = request.GET.get('code', None)
        url = client.oauth.authorize_url(request.url)

        if code:
            try:
                user_info = client.oauth.get_user_info(code)
            except Exception as e:
                print e.errmsg, e.errcode
                abort(403)
            else:
                session['user_info'] = user_info
        else:
            return redirect(url)

        return method(*args, **kwargs)
    
    return warpper