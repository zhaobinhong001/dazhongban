from allauth.account import app_settings as account_app_settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from rest_framework import status

from .test_base import BaseAPITestCase


class APITestAuth(TestCase, BaseAPITestCase):
    """
    Case #1:
    - user profile: defined
    - custom registration: backend defined
    """

    USERNAME = 'person'
    PASS = 'person'
    EMAIL = "person1@world.com"
    NEW_PASS = 'new-test-pass'
    REGISTRATION_VIEW = 'rest_auth.runtests.RegistrationView'

    # data without user profile
    REGISTRATION_DATA = {
        "username": USERNAME,
        "password1": PASS,
        "password2": PASS
    }

    REGISTRATION_DATA_WITH_EMAIL = REGISTRATION_DATA.copy()
    REGISTRATION_DATA_WITH_EMAIL['email'] = EMAIL

    BASIC_USER_DATA = {
        'first_name': "John",
        'last_name': 'Smith',
        'email': EMAIL
    }
    USER_DATA = BASIC_USER_DATA.copy()
    USER_DATA['newsletter_subscribe'] = True

    def setUp(self):
        self.init()

    def _generate_uid_and_token(self, user):
        ''''''
        result = {}
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode

        result['uid'] = urlsafe_base64_encode(force_bytes(user.pk))
        result['token'] = default_token_generator.make_token(user)
        return result

    def test_login_failed_verify_validation(self):
        payload = {
            "mobile": '',
            "verify": self.PASS
        }
        resp = self.post(self.login_url, data=payload, status_code=400)
        self.assertEqual(resp.json['non_field_errors'][0], u'Must include "email" and "password".')

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=account_app_settings.AuthenticationMethod.USERNAME)
    def test_login_failed_mobile_validation(self):
        payload = {
            "mobile": '',
            "verify": self.PASS
        }

        resp = self.post(self.login_url, data=payload, status_code=400)
        self.assertEqual(resp.json['non_field_errors'][0], u'Must include "username" and "password".')

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=account_app_settings.AuthenticationMethod.USERNAME_EMAIL)
    def test_login_failed_username_email_validation(self):
        payload = {
            "password": self.PASS
        }

        resp = self.post(self.login_url, data=payload, status_code=400)
        self.assertEqual(resp.json['non_field_errors'][0], u'Must include either "username" or "email" and "password".')

    def test_user_details(self):
        user = get_user_model().objects.create_user(self.USERNAME, self.EMAIL, self.PASS)
        payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }
        self.post(self.login_url, data=payload, status_code=200)
        self.token = self.response.json['key']
        self.get(self.user_url, status_code=200)

        self.patch(self.user_url, data=self.BASIC_USER_DATA, status_code=200)
        user = get_user_model().objects.get(pk=user.pk)
        self.assertEqual(user.first_name, self.response.json['first_name'])
        self.assertEqual(user.last_name, self.response.json['last_name'])
        self.assertEqual(user.email, self.response.json['email'])

    def test_registration(self):
        user_count = get_user_model().objects.all().count()

        # test empty payload
        self.post(self.register_url, data={}, status_code=400)

        result = self.post(self.register_url, data=self.REGISTRATION_DATA, status_code=201)
        self.assertIn('key', result.data)
        self.assertEqual(get_user_model().objects.all().count(), user_count + 1)

        new_user = get_user_model().objects.latest('id')
        self.assertEqual(new_user.username, self.REGISTRATION_DATA['username'])

        self._login()
        self._logout()

    @override_settings(
        ACCOUNT_EMAIL_VERIFICATION='mandatory',
        ACCOUNT_EMAIL_REQUIRED=True,
        ACCOUNT_EMAIL_CONFIRMATION_HMAC=False
    )
    def test_registration_with_verify_verification(self):
        user_count = get_user_model().objects.all().count()
        mail_count = len(mail.outbox)

        # test empty payload
        self.post(
            self.register_url,
            data={},
            status_code=status.HTTP_400_BAD_REQUEST
        )

        result = self.post(
            self.register_url,
            data=self.REGISTRATION_DATA_WITH_EMAIL,
            status_code=status.HTTP_201_CREATED
        )
        self.assertNotIn('key', result.data)
        self.assertEqual(get_user_model().objects.all().count(), user_count + 1)
        self.assertEqual(len(mail.outbox), mail_count + 1)
        new_user = get_user_model().objects.latest('id')
        self.assertEqual(new_user.username, self.REGISTRATION_DATA['username'])

        # email is not verified yet
        payload = {
            "username": self.USERNAME,
            "password": self.PASS
        }
        self.post(
            self.login_url,
            data=payload,
            status=status.HTTP_400_BAD_REQUEST
        )

        # verify email
        email_confirmation = new_user.emailaddress_set.get(email=self.EMAIL) \
            .emailconfirmation_set.order_by('-created')[0]
        self.post(
            self.veirfy_email_url,
            data={"key": email_confirmation.key},
            status_code=status.HTTP_200_OK
        )

        # try to login again
        self._login()
        self._logout()
