# -*- coding: utf-8 -*-
# dashboard/boxes.py

from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from suit_dashboard.box import Box, Item


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
        chart_options = {
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
                'text': _('总用户数量'),
                'href': 'data',
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
                            "y": 70
                        },
                        {
                            "name": _("本周新增"),
                            "y": 40,
                            "sliced": True,
                            "selected": True
                        },
                        {
                            "name": _("昨日新增"),
                            "y": 10
                        }
                    ]
                }
            ]
        }

        # Create the chart item
        item_chart = Item(
            html_id='user',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


class Authentication(Box):
    def get_items(self):
        chart_options = {
            'chart': {
                'type': 'pie',
                'height': 300,
            },
            'title': {
                'text': _('')
            },
            'credits': {
                'enabled': True,
                'text': _('已认证用户量'),
                'href': 'data',
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
            'colors': ['#058DC7', '#50B432', '#ED561B', '#DDDF  00',
                '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
            'series': [
                {
                    "name": "Brands",
                    "colorByPoint": True,
                    "data": [
                        {
                            "name": _('历史总数'),
                            "y": 100
                        },
                        {
                            "name": _("本周新增"),
                            "y": 40,
                            "sliced": True,
                            "selected": True
                        },
                        {
                            "name": _("昨日新增"),
                            "y": 10
                        }
                    ]
                }
            ]
        }

        # Create the chart item
        item_chart = Item(
            html_id='authentication',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


class SettledEnterprise(Box):
    def get_items(self):
        chart_options = {
            'chart': {
                'type': 'pie',
                'height': 300,
            },
            'title': {
                'text': _('')
            },
            'credits': {
                'enabled': True,
                'text': _('总入驻企业数量'),
                'href': 'data',
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
            'colors': ['#058DC7', '#50B432', '#ED561B', '#DDDF  00',
                '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
            'series': [
                {
                    "name": "Brands",
                    "colorByPoint": True,
                    "data": [
                        {
                            "name": _('历史总数'),
                            "y": 200
                        },
                        {
                            "name": _("本周新增"),
                            "y": 40,
                            "sliced": True,
                            "selected": True
                        },
                        {
                            "name": _("昨日新增"),
                            "y": 10
                        }
                    ]
                }
            ]
        }

        # Create the chart item
        item_chart = Item(
            html_id='settledEnterprise',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


class Signatures(Box):
    def get_items(self):
        chart_options = {
            'chart': {
                'type': 'pie',
                'height': 300,
            },
            'title': {
                'text': _('')
            },
            'credits': {
                'enabled': True,
                'text': _('用户签名次数'),
                'href': 'data',
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
            'colors': ['#058DC7', '#50B432', '#ED561B', '#DDDF  00',
                '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
            'series': [
                {
                    "name": "Brands",
                    "colorByPoint": True,
                    "data": [
                        {
                            "name": _('历史总数'),
                            "y": 70
                        },
                        {
                            "name": _("本周新增"),
                            "y": 40,
                            "sliced": True,
                            "selected": True
                        },
                        {
                            "name": _("昨日新增"),
                            "y": 10
                        }
                    ]
                }
            ]
        }

        # Create the chart item
        item_chart = Item(
            html_id='signatures',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


class Evidences(Box):
    def get_items(self):
        chart_options = {
            'chart': {
                'type': 'pie',
                'height': 300,
            },
            'title': {
                'text': _('')
            },
            'credits': {
                'enabled': True,
                'text': _('用户取证次数'),
                'href': 'data',
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
            'colors': ['#058DC7', '#50B432', '#ED561B', '#DDDF  00',
                '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
            'series': [
                {
                    "name": "Brands",
                    "colorByPoint": True,
                    "data": [
                        {
                            "name": _('历史总数'),
                            "y": 70
                        },
                        {
                            "name": _("本周新增"),
                            "y": 40,
                            "sliced": True,
                            "selected": True
                        },
                        {
                            "name": _("昨日新增"),
                            "y": 10
                        }
                    ]
                }
            ]
        }

        # Create the chart item
        item_chart = Item(
            html_id='evidences',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


class BasicLine(Box):
    def get_items(self):
        chart_options = {
            "title": {
                "text": _('总用户数量'),
                "x": -20
            },
            "subtitle": {
                "text": "",
                "x": -20
            },
            "xAxis": {
                'title': {
                    'text': '时间'
                },
                "categories": [
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec"
                ]
            },
            "yAxis": {
                "title": {
                    "text": "数量"
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
                "valueSuffix": _('人')
            },
            "legend": {
                "layout": "vertical",
                "align": "right",
                "verticalAlign": "middle",
                "borderWidth": 0
            },
            "series": [
                {
                    "name": _('用户量'),
                    "data": [
                        7,
                        6.9,
                        9.5,
                        14.5,
                        18.2,
                        21.5,
                        25.2,
                        26.5,
                        23.3,
                        18.3,
                        13.9,
                        9.6
                    ]
                }
            ]
        }

        # Create the chart item
        item_chart = Item(
            html_id='basicLine',
            # name=_('数据统计'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]
