# coding:utf-8
from __future__ import unicode_literals

from django.db import models

TRANSFER_TYPE = (
    ('198', '收款'),
    ('199', '转账'),
)


# 转账表
class Transfer(models.Model):
    parent_id = models.IntegerField(verbose_name=u'编号')
    transfer_type = models.CharField(verbose_name=u'转账类型', choices=TRANSFER_TYPE, max_length=100, default=199)
    transfer_money = models.DecimalField(verbose_name=u'转账金额', max_digits=10, decimal_places=2)
    receivables_bank = models.CharField(verbose_name=u'收款银行', max_length=30, )
    receivables_lastNum = models.IntegerField(verbose_name='收款尾号')
    drawee = models.CharField(verbose_name=u'付款人', max_length=100)
    Payee = models.CharField(verbose_name=u'收款人', max_length=100, default='Null')
    drawee_bank = models.CharField(verbose_name=u'付款银行', max_length=30)
    drawee_lastNum = models.IntegerField(verbose_name=u'付款尾号')
    receivables_mark = models.TextField(verbose_name=u'转账备注', null=True)
    application_time = models.DateTimeField(verbose_name=u'申请时间', auto_now_add=True)
    receipt_time = models.DateTimeField(verbose_name=u'签收时间', auto_now_add=True)
    confirm_transfer = models.BooleanField(verbose_name=u'确认转账', default=False)
    confirm_receipt = models.BooleanField(verbose_name=u'确认收款', default=False)

    def __unicode__(self):
        return '%s %s %s' % (self.receivables_bank, self.drawee, self.drawee_bank)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = (u'转账记录')
        verbose_name_plural = (u'转账记录')
