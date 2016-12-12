# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import unicodedata

from django import forms
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError

from service.consumer.models import Profile
from service.kernel.utils.sms import check_verify_code
from .adapter import get_adapter
from .utils import user_email, user_field, user_username


class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs):
        render_value = kwargs.pop('render_value', False)
        kwargs['widget'] = forms.PasswordInput(render_value=render_value,
            attrs={'placeholder':
                _(kwargs.get("label"))})
        super(PasswordField, self).__init__(*args, **kwargs)


class SetPasswordField(PasswordField):
    def clean(self, value):
        value = super(SetPasswordField, self).clean(value)
        value = get_adapter().clean_password(value)
        return value


class SignupForm(forms.Form):
    mobile = forms.CharField(label=_(u"手机号"), max_length=20, required=True)
    verify = forms.CharField(label=_(u"验证码"), max_length=10, required=False)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(forms.Form, self).clean()

        if not self.cleaned_data.get("mobile", None):
            raise ValidationError({'mobile': _("手机号码不能为空.")})

        if not self.cleaned_data.get("verify", None):
            raise ValidationError({'verify': _("验证码不能为空.")})

        # 判断手机是否匹配规格
        if not re.match(r'^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$',
                self.cleaned_data.get("mobile")):
            raise ValidationError({'mobile': "手机号码格式不匹配."})

        # 判断验证码
        verify_status = check_verify_code(self.cleaned_data["mobile"], self.cleaned_data["verify"])

        if not verify_status:
            raise ValidationError(_(u'验证码错误'))

        # 判断手机是否注册过
        if get_user_model()._default_manager.filter(mobile=self.cleaned_data['mobile']).exists():
            raise ValidationError(_("用户手机号码已经注册过."))

        return self.cleaned_data

    def save(self, request):
        user = get_user_model()()
        self.save_user(request, user, self)

        return user

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        data = form.cleaned_data

        mobile = data.get('mobile')
        verify = data.get('verify')

        if verify:
            user_field(user, 'verify', verify)

        if mobile:
            user_field(user, 'mobile', mobile)

        self.populate_username(request, user)

        if commit:
            user.save()

        Profile.objects.get_or_create(owner=user)

        return user

    def populate_username(self, request, user):
        """
        Fills in a valid username, if required and missing.  If the
        username is already present it is assumed to be valid
        (unique).
        """
        mobile = user_field(user, 'mobile')
        email = user_email(user)
        username = user_username(user)
        user_username(user, username or self.generate_unique_username([mobile, email, 'user']))

    def generate_unique_username(self, txts, regex=None):
        return generate_unique_username(txts, regex)


def _generate_unique_username_base(txts, regex=None):
    username = None
    regex = regex or '[^\w\s@+.-]'
    for txt in txts:
        if not txt:
            continue
        username = unicodedata.normalize('NFKD', force_text(txt))
        username = username.encode('ascii', 'ignore').decode('ascii')
        username = force_text(re.sub(regex, '', username).lower())
        username = username.split('@')[0]
        username = username.strip()
        username = re.sub('\s+', '_', username)

        if username:
            break

    return username or 'user'


def generate_unique_username(txts, regex=None):
    username = _generate_unique_username_base(txts, regex)
    User = get_user_model()
    max_length = 20
    i = 0

    while True:
        try:
            if i:
                pfx = str(i + 1)
            else:
                pfx = ''

            ret = username[0:max_length - len(pfx)] + pfx
            query = {'username' + '__iexact': ret}
            User.objects.get(**query)

            i += 1
        except User.DoesNotExist:
            return ret
