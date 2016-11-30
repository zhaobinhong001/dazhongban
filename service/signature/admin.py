from daterange_filter.filter import DateTimeRangeFilter
from django.contrib import admin

from .models import Signature


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    list_display = ('created', 'signs', 'owner')
    list_filter = (('created', DateTimeRangeFilter),)
    list_display_links = None

    def has_add_permission(self, request):
        pass

    class Media:
        js = ['/admin/jsi18n/']
