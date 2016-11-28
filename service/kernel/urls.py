# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view
from .views.certufucate import CertufucateViewSet
from .views.transfer import TransferViewSet
from .views.consumption import ConsumptionViewSet
from service.kernel.views.enterprise import EnterproseViewSet

from .views.goods import GoodsViewSet

router = DefaultRouter()

# router.register(r'goods', GoodsViewSet, base_name='goods')
# router.register(r'aaa', GoodsViewSet, base_name='aa')
# router.register(r'first', FirstViewSet, base_name='first')
# router.register(r'trade', TradeViewSet, base_name='trade')
# router.register(r'bests', BestsViewSet, base_name='bests')
# router.register(r'query', QueryViewSet, base_name='query')

# router.register(r'random', RandomViewSet, base_name='random')
# router.register(r'search', SearchViewSet)

# router.register(r'category', CategoryViewSet)
# router.register(r'feedback', FeedbackViewSet)
# router.register(r'location', LocationViewSet)

# router.register(r'recommend', RecommendViewSet, base_name='recommend')
# router.register(r'watchword', WatchwordViewSet)

# # 采集接口
# router.register(r'collect', CollectViewSet, base_name='collect')
# router.register(r'preselection', PreselectionViewSet, base_name='preselection')

# children_router = routers.NestedSimpleRouter(router, r'category', lookup='category')
# children_router.register(r'children', ChildrenViewSet, base_name='category-children')

router.register(r'certufucates', CertufucateViewSet, base_name='certufucate')
router.register(r'transfer', TransferViewSet, base_name='transfer')
router.register(r'consumption', ConsumptionViewSet, base_name='Consumption')

# 企业用户
router.register(r'enterprise', EnterproseViewSet, base_name='enterprise')

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = (
    url(r'^', include(router.urls, namespace='v1.0')),
    url(r'^me/', include('service.consumer.urls')),

    url(r'^auth/', include('service.restauth.urls')),
    url(r'^user/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/$', schema_view),
)
