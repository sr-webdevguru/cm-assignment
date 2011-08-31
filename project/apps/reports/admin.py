from django.contrib import admin

from apps.reports.models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'global_status', 'report_user', 'report_resort')
    list_filter = ('global_status', 'report_user')
    search_fields = ('global_status', 'report_user')
    ordering = ('report_id',)


admin.site.register(Report, ReportAdmin)
