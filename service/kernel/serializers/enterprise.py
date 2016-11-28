from __future__ import unicode_literals

from rest_framework import serializers
from service.kernel.models.enterprise import EnterpriseUser


class enterpriseSerialzer(serializers.ModelSerializer):
    class Meta:
        model = EnterpriseUser
        fields = '__all__'
