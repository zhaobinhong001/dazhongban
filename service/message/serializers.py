from rest_framework import serializers

from .models import Groups


class GroupsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Groups
        fields = ('id', 'name',)


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Groups
        fields = ('id', 'name',)
