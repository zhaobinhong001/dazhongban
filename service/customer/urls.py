# # -*- coding: utf-8 -*-
# # customer/urls.py
#
# from __future__ import unicode_literals
# from django.contrib.admin.sites import AdminSite
# from django.conf.urls import url
# from .views import HomeView
#
#
# class CustomerSite(AdminSite):
#     """A Django AdminSite to allow registering custom dashboard views."""
#
#     def get_urls(self):
#         urls = super(CustomerSite, self).get_urls()
#         custom_urls = [
#             url(r'^$', self.admin_view(HomeView.as_view()), name='test'),
#             # url(r'^data/$', self.admin_view(LineView.as_view()), name='data'),
#         ]
#
#         del urls[0]
#         return custom_urls + urls
# #
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from .views import HomeView
# from .views import (
#     LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView,
#     PasswordResetView, SocialView
# )

urlpatterns = (
    # url(r'^password/reset/$', PasswordResetView.as_view(), name='rest_password_reset'),
    # url(r'^password/change/$', PasswordChangeView.as_view(), name='rest_password_change'),
    url(r'^$',HomeView.as_view(), name='test'),
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    # url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    # url(r'^login/$', LoginView.as_view(), name='rest_login'),
    # url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    # url(r'^social/$', SocialView.as_view(), name='rest_social_bind'),
    # url(r'^registration/', include(registration_urls)),
)
