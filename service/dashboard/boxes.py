# -*- coding: utf-8 -*-
# dashboard/boxes.py

from __future__ import unicode_literals

import datetime

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from suit_dashboard.box import Box, Item

from service.kernel.models.enterprise import EnterpriseUser

# 用户信息

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
weekday = today - datetime.timedelta(days=7)
userTitle = '总用户数量'


def userDate():
    if get_user_model().objects.all().count():
        userlen = get_user_model().objects.all().count()
        Yesterdaylen = get_user_model().objects.filter(date_joined__range=(yesterday, today)).count()
        weeklen = get_user_model().objects.filter(date_joined__range=(weekday, today)).count()
    else:
        userlen = 0
        Yesterdaylen = 0
        weeklen = 0
    return {'userlen': userlen, 'Yesterdaylen': Yesterdaylen, 'weeklen': weeklen}


# pie chart

# @title        图标题
# @href         链接
# @hislen       历史总数
# @yesterdaylen 昨日新增
# @weeklen      本周新增
def pieOption(title, href, hislen, yesterdaylen, weeklen):
    data = {
        'chart': {
            'type': 'pie',
            'height': 300,
        },
        'colors': [
            'red',
            'blue',
            'yellow',
            '#1aadce',
            '#492970',
            '#f28f43',
            '#77a1e5',
            '#c42525',
            '#a6c96a'
        ],
        'title': {
            'text': _('')
        },
        'credits': {
            'enabled': True,
            'text': _(title),
            'href': href,
            'position': {
                'align': 'center',
                'verticalAlign': 'bottom',
                # 'x':100,
                # 'y': -10
            },

        },
        'tooltip': {
            'percentageDecimals': 1
        },
        'legend': {
            'enabled': False
        },
        'plotOptions': {
            'pie': {
                'allowPointSelect': True,
                'cursor': 'pointer',
                # 'dataLabels': {
                #     'enabled': True,
                #     'format': '<b>{point.name}</b>: {point.percentage:.1f} %',
                # }
            },
            'series': {
                'stacking': '',  # normal
            }
        },
        'series': [
            {
                "name": "Brands",
                "colorByPoint": True,
                "data": [
                    {
                        "name": _('历史总数'),
                        "y": hislen
                    },
                    {
                        "name": _("本周新增"),
                        "y": weeklen,
                        "sliced": True,
                        "selected": True
                    },
                    {
                        "name": _("昨日新增"),
                        "y": yesterdaylen
                    }
                ]
            }
        ]
    }
    return data


# line chart
# user 用户信息
def userLineDate():
    now = datetime.datetime.now()
    today_year = now.year
    last_year = int(now.year) - 1
    today_year_months = range(1, now.month + 1)
    last_year_months = range(now.month + 1, 13)
    data_list_lasts = []

    for last_year_month in last_year_months:
        date_list = '%s-%s' % (last_year, last_year_month)

        data_list_lasts.append(date_list)

    data_list_todays = []

    for today_year_month in today_year_months:
        data_list = '%s-%s' % (today_year, today_year_month)

        data_list_todays.append(data_list)

    data_year_month = data_list_lasts + data_list_todays

    # ina = get_user_model().objects.filter(date_joined__year='2016', date_joined__month='12')
    ary = []
    if (get_user_model().objects):
        for myd in data_year_month:
            ye = myd.split('-')
            ina = get_user_model().objects.filter(date_joined__year=ye[0], date_joined__month=ye[1]).count()
            ary.append(ina)
    else:
        ary = []

    return {'ary': ary, 'data_year_month': data_year_month}


# @title 线图标题
# @ary   12个月对应数据 type：array

def lineOption(title, ary, month=userLineDate()['data_year_month'], xAxis='时间', yAxis='数量', tooltipVal='人',
        lineName='用户量'):
    data = {
        "title": {
            "text": _(title),
            "x": -20
        },
        "subtitle": {
            "text": "",
            "x": -20
        },
        "xAxis": {
            'title': {
                'text': xAxis
            },
            "categories": month
        },
        "yAxis": {
            "title": {
                "text": yAxis
            },
            "plotLines": [
                {
                    "value": 0,
                    "width": 1,
                    "color": "#808080"
                }
            ]
        },
        'credits': {
            'enabled': False,

        },
        "tooltip": {
            "valueSuffix": _(tooltipVal)
        },
        "legend": {
            "layout": "vertical",
            "align": "right",
            "verticalAlign": "middle",
            "borderWidth": 0
        },
        "series": [
            {
                "name": _(lineName),
                "data": ary
            }
        ]
    }
    return data


# 总用户数量 chart date

class User(Box):
    # def get_title(self):
    #     return _('数据统计')

    # def get_description(self):
    #     return _('Information about the hosting machine for my website.')

    # The get_items function is the main function here. It will define
    # what are the contents of the box.
    def get_items(self):
        # Retrieve and format uptime (will not work on Windows)
        # with open('uptime.txt') as f:

        # s = timedelta(seconds=psutil.boot_time()).total_seconds()
        # uptime = _('%d 天, %d 小时, %d 分, %d 秒') % (
        #     s // 86400, s // 3600 % 24, s // 60 % 60, s % 60)

        # Create a first item (box's content) with the machine info
        # item_info = Item(
        #     html_id='sysspec', name=_('系统'),
        #     display=Item.AS_TABLE,
        #     # Since we use AS_TABLE display, value must be a list of tuples
        #     value=(
        #         (_('主机名称'), platform.node()),
        #         (_('系统平台'), '%s, %s, %s' % (
        #             platform.system(),
        #             ' '.join(platform.linux_distribution()),
        #             platform.release())),
        #         (_('核心架构'), ' '.join(platform.architecture())),
        #         (_('处理器'), platform.processor()),
        #         (_('Python 版本'), platform.python_version()),
        #         # (_('Uptime'), uptime)
        #
        #     ),
        #     classes='table-bordered table-condensed '
        #             'table-hover table-striped'
        # )

        # Retrieve RAM and CPU data
        # ram = psutil.virtual_memory().percent
        # cpu = psutil.cpu_percent()

        # # Green, orange, red or grey color for usage/idle
        # green, orange, red, grey = '#00FF38', '#FFB400', '#FF3B00', '#EBEBEB'
        #
        # ram_color = green  # default
        # if ram >= 75:
        #     ram_color = red
        # elif ram >= 50:
        #     ram_color = orange
        #
        # cpu_color = green  # default
        # if cpu >= 75:
        #     cpu_color = red
        # elif cpu >= 50:
        #     cpu_color = orange

        # Now create a chart to display CPU and RAM usage
        chart_options = pieOption(userTitle, 'data', userDate()['userlen'], userDate()['Yesterdaylen'],
            userDate()['weeklen'])

        # Create the chart item
        item_chart = Item(
            html_id='user',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


class BasicLine(Box):
    def get_items(self):
        chart_options = lineOption('总用户', userLineDate()['ary'], userLineDate()['data_year_month'])

        # Create the chart item
        item_chart = Item(
            html_id='basicLine',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


# 已认证用户pie chart date
# pieOption('已认证用户量','aution',userlen, Yesterdaylen, weeklen)
class Authentication(Box):
    def get_items(self):
        chart_options = pieOption('已认证用户量', 'aution', userDate()['userlen'], userDate()['Yesterdaylen'],
            userDate()['weeklen'])

        # Create the chart item
        item_chart = Item(
            html_id='authentication',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


# 已认证用户line chart date
# lineOption('已认证用户量', ary, data_year_month)
class AutionLine(Box):
    def get_items(self):
        chart_options = lineOption('已认证用户量', userLineDate()['ary'], userLineDate()['data_year_month'])

        # Create the chart item
        item_chart = Item(
            html_id='autionLine',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


# 总入驻企业数量 chart date

# 入驻企业信息
def entDate():
    if (EnterpriseUser.objects.all().count()):
        entlen = EnterpriseUser.objects.all().count()
        yesterdayenlen = EnterpriseUser.objects.filter(settled_date__range=(yesterday, today)).count()
        weekenlen = EnterpriseUser.objects.filter(settled_date__range=(weekday, today)).count()
    else:
        entlen = 0
        yesterdayenlen = 0
        weekenlen = 0
    return {'entlen': entlen, 'yesterdayenlen': yesterdayenlen, 'weekenlen': weekenlen}


enterpriseUserTitle = '总入驻企业数量'


class SettledEnterprise(Box):
    def get_items(self):
        chart_options = pieOption(enterpriseUserTitle, 'seten', entDate()['entlen'], entDate()['yesterdayenlen'],
            entDate()['weekenlen'])

        # Create the chart item
        item_chart = Item(
            html_id='settledEnterprise',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


# 入驻企业数量 line data

setenTitle = '总入驻企业数量'


def setLineDate():
    setenAry = []
    if (EnterpriseUser.objects):
        for seten in userLineDate()['data_year_month']:
            seten = seten.split('-')
            setA = EnterpriseUser.objects.filter(settled_date__year=seten[0], settled_date__month=seten[1]).count()
            setenAry.append(setA)
    else:
        setenAry = []
    return {'setenAry': setenAry}


# create 入驻企业数量 line
class SetEnLine(Box):
    def get_items(self):
        chart_options = lineOption(setenTitle, setLineDate()['setenAry'], userLineDate()['data_year_month'])

        # Create the chart item
        item_chart = Item(
            html_id='setEnLine',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


# 用户签名次数 pie chart date
# pieOption('用户签名次数','sign',userlen, Yesterdaylen, weeklen)

class Signatures(Box):
    def get_items(self):
        chart_options = pieOption('用户签名次数', 'sign', userDate()['userlen'], userDate()['Yesterdaylen'],
            userDate()['weeklen'])

        # Create the chart item
        item_chart = Item(
            html_id='signatures',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


# 用户签名次数 line chart date
# lineOption('用户签名次数', setenAry, data_year_month,  yAxis='次')
class SignLine(Box):
    def get_items(self):
        chart_options = lineOption('用户签名次数', setLineDate()['setenAry'], userLineDate()['data_year_month'], yAxis='次')

        # Create the chart item
        item_chart = Item(
            html_id='signLine',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


# 用户取证次数 pie chart date
# pieOption('用户取证次数', 'evid', userlen, Yesterdaylen, weeklen)
class Evidences(Box):
    def get_items(self):
        chart_options = pieOption('用户取证次数', 'evid', userDate()['userlen'], userDate()['Yesterdaylen'],
            userDate()['weeklen'])

        # Create the chart item
        item_chart = Item(
            html_id='evidences',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


# 用户取证次数 line chart date
# lineOption('用户取证次数', setenAry, data_year_month,  yAxis='次')
class EvidLine(Box):
    def get_items(self):
        chart_options = lineOption('用户取证次数', setLineDate()['setenAry'], userLineDate()['data_year_month'], yAxis='次')

        # Create the chart item
        item_chart = Item(
            html_id='evidLine',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]
