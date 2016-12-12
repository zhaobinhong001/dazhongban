# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import short_url
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.contenttypes import fields as generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ProcessedImageField
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel
from pilkit.processors import ResizeToFill
from rest_framework.serializers import ValidationError


class AbstractActionType(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, blank=True, default=None)
    content_object = generic.GenericForeignKey('content_type', 'object_id', )

    def validate_unique(self):
        if (self.__class__.objects.filter(owner=self.owner, object_id=self.object_id,
                content_type=self.content_type).exists()):
            raise ValidationError({'detail': 'The record already exists. '})

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password,
            is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()

        if not username:
            raise ValueError('The given username must be set')

        # email = self.normalize_email(email)

        user = self.model(username=username,
            is_staff=is_staff, is_active=True,
            is_superuser=is_superuser,
            date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, False, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True, **extra_fields)


class CustomUser(AbstractUser):
    """
    Concrete class of AbstractEmailUser.
    Use this if you don't need to extend EmailUser.
    """

    REQUIRED_FIELDS = []
    GENDER_CHOICES = (('male', '男'), ('female', '女'))
    mobile = models.CharField(_(u'手机号码'), max_length=25, db_index=True, blank=True)
    verify = models.CharField(_(u'短信码'), max_length=5, blank=True)
    device = models.CharField(_(u'设备号'), max_length=100, blank=False, null=False)
    level = models.CharField(_(u'用户等级'), max_length=100, blank=False, null=False)

    objects = CustomUserManager()

    def short(self):
        short_url.encode_url(self.pk)


class Profile(models.Model):
    '''
    该接口更新接受PUT方法

    性别字段英文对应汉字为:
    male:男
    female:女
    提交的数据要用英文.获取时候api也是英文, 要客户端自己做下转换.
    '''
    GENDER_CHOICES = (('male', '男'), ('female', '女'))

    owner = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True, db_index=True, related_name='profile')
    name = models.CharField(verbose_name=_(u'姓名'), blank=True, max_length=255, db_index=True)
    nick = models.CharField(verbose_name=_(u'昵称'), blank=True, null=True, max_length=255, db_index=True)
    phone = models.CharField(verbose_name=_(u'电话'), default='', blank=True, max_length=64)
    gender = models.CharField(verbose_name=_(u'性别'), max_length=10, choices=GENDER_CHOICES, default=u'male')
    birthday = models.DateField(_(u'生日'), blank=True, null=True)
    # alipay = models.CharField(verbose_name=_(u'支付宝'), max_length=100, blank=True)
    # payment = models.DecimalField(verbose_name=_(u'已经提现'), default=0.00, max_digits=10, decimal_places=2)
    # balance = models.DecimalField(verbose_name=_(u'帐户余额'), default=0.00, max_digits=10, decimal_places=2)
    # total = models.DecimalField(verbose_name=_(u'帐户总额'), default=0.00, max_digits=10, decimal_places=2)
    avatar = ProcessedImageField(verbose_name=_(u'头像'), upload_to='avatar', processors=[ResizeToFill(320, 320)],
        format='JPEG', null=True)

    friend_verify = models.BooleanField(verbose_name=_(u'加好友时是否验证'), default=False)
    mobile_verify = models.BooleanField(verbose_name=_(u'是否允许手机号查找'), default=False)
    name_public = models.BooleanField(verbose_name=_(u'是否公开姓名'), default=False)

    @property
    def qr(self):
        return ''

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'profile')
        verbose_name_plural = _(u'profiles')


class Address(TimeStampedModel):
    '''
    用户地址信息

    '''
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
    city = models.CharField(verbose_name=_(u'城市'), blank=True, max_length=255, db_index=True)
    area = models.CharField(verbose_name=_(u'市区'), blank=True, null=True, max_length=255, db_index=True)
    address = models.CharField(verbose_name=_(u'详细地址'), blank=True, null=True, max_length=255, db_index=True)
    default = models.BooleanField(verbose_name=_('默认地址'), default=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'用户地址')
        verbose_name_plural = _(u'用户地址')


class Contains(TimeStampedModel):
    '''
    用户通讯录

    '''
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    contains = models.TextField(_(u'手机通讯录数据'), default='')

    def __unicode__(self):
        return self.owner

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'手机通讯录')
        verbose_name_plural = _(u'手机通讯录')


class Contact(TimeStampedModel, StatusModel):
    '''
    用户通讯录

    '''
    STATUS = Choices(('invite', '邀请'), ('confirm', '确认'))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('好友'), default='', related_name='friends')
    black = models.BooleanField(_('是否黑名单'), default=False)
    alias = models.CharField(_(u'备注别名'), max_length=100, default='')
    hide = models.BooleanField(_('别人不可见真名'), default=False)

    def __unicode__(self):
        return self.owner.username + '-' + self.friend.username

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'用户通讯录')
        verbose_name_plural = _(u'用户通讯录')


class Bankcard(TimeStampedModel):
    '''
    银行卡信息

    '''
    TYPE_CHOICES = (('储蓄卡', '储蓄卡'),)
    FLAG_CHOICES = (('收', '收'),)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
    bank = models.CharField(verbose_name=_(u'所属银行'), blank=True, max_length=50, default='')
    card = models.CharField(verbose_name=_(u'银行卡号'), blank=True, max_length=50, default='')
    suffix = models.CharField(verbose_name=_(u'卡号后缀'), max_length=10, default='')
    type = models.CharField(verbose_name=_('卡片类型'), max_length=10, choices=TYPE_CHOICES, default='')
    flag = models.CharField(verbose_name=_('卡片用途'), max_length=10, choices=FLAG_CHOICES, default='')

    def __unicode__(self):
        return '%s - %s' % (self.bank, self.card)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'用户银行卡')
        verbose_name_plural = _(u'用户银行卡')


class Settings(models.Model):
    '''
    该接口更新接受PUT方法

    电话号码绑定状态:
    fales: 未绑定
    true: 已绑定
    默认: 未绑定
    身份认证状态:
    fales: 未认证
    true: 已认证
    默认: 未认证
    证件类型字段英文对应汉字为:
    identity:居民身份证
    driver:驾驶证
    officers:军官证
    passport:护照
    提交的数据要用英文.获取时候api也是英文, 要客户端自己做下转换.
    '''
    GENDER_CHOICES = (('identity', '居民身份证'), ('driver', '驾驶证'), ('officers', '军官证'), ('passport', '护照'))

    owner = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True, db_index=True, related_name='settings')
    name = models.CharField(verbose_name=_(u'姓名'), blank=True, max_length=255, db_index=True)
    nick = models.CharField(verbose_name=_(u'马甲'), blank=True, null=True, max_length=255, db_index=True)
    phone = models.CharField(verbose_name=_(u'电话'), default='', blank=True, max_length=64)
    type_phone = models.BooleanField(verbose_name=_(u'电话号码绑定状态'), default=False)
    id_card = models.CharField(verbose_name=_(u'证件号码'), default='', blank=True, max_length=64)
    document_type = models.CharField(verbose_name=_(u'证件类型'), max_length=10, choices=GENDER_CHOICES, default='identity')
    id_identity = models.BooleanField(verbose_name=_(u'身份认证'), default=False)
    avatar = ProcessedImageField(verbose_name=_(u'头像'), upload_to='avatar', processors=[ResizeToFill(320, 320)],
        format='JPEG', null=True)
    friend_verify = models.BooleanField(verbose_name=_(u'加好友时是否验证'), default=False)
    mobile_verify = models.BooleanField(verbose_name=_(u'是否允许手机号查找'), default=False)
    public_name = models.BooleanField(verbose_name=_(u'是否公开姓名'), default=False)



    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _(u'settings')
        verbose_name_plural = _(u'settings')
