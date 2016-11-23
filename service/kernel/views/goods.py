# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Goods
from ..serializers.goods import GoodsSerializer


class GoodsViewSet(viewsets.ModelViewSet):
    '''
    商品接口
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    permission_classes = (IsAuthenticated,)
    # allowed_methods = ('POST', 'OPTIONS', 'HEAD')
