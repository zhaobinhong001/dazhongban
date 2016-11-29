from __future__ import unicode_literals

from django.conf import settings
from django.db import models


class Signature(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='signatures')
