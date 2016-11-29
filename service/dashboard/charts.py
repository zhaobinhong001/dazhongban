# -*- coding: utf-8 -*-
# dashboard/charts.py

from __future__ import unicode_literals
import psutil
from django.utils.translation import ugettext_lazy as _
from suit_dashboard.decorators import refreshable

@refreshable
def machine_usage_chart():
    # Retrieve RAM and CPU data
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()

    # ... like before (save you some scrolling)

    return chart_options