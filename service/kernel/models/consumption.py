# coding:utf-8
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel, StatusModel

CONTRACT_TYPE = (
    ('receipt', '收据'),
    ('borrow', '借条'),
    ('owe', '欠条'),
)


# 合约表
class Contract(TimeStampedModel, StatusModel):
    STATUS = (('sender', '发送'), ('receiver', '接受'),)

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, default='', related_name='contract_sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, default='', related_name='contract_receiver', blank=True,
                                 null=True)

    type = models.CharField(verbose_name=u'消费类型', max_length=100, default=0, choices=CONTRACT_TYPE)
    mobile = models.CharField(verbose_name=u'手机号', max_length=100, default='')
    amount = models.DecimalField(verbose_name=u'交易金额', max_digits=10, decimal_places=2)
    summary = models.CharField(verbose_name=u'原因', max_length=300)
    make_date = models.DateTimeField(verbose_name=u'操作时间', blank=True, null=True)

    def __unicode__(self):
        return self.summary

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'合约记录')
        verbose_name_plural = _(u'合约记录')
