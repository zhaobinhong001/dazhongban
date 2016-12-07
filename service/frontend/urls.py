from django.conf.urls import url

from .views import q

urlpatterns = [
    url(r'^q/(?P<uid>.*)/$', q, name='q'),
]
