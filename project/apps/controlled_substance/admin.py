from django.contrib import admin

from apps.controlled_substance.models import StockAssignment


class StockAssignmentAdmin(admin.ModelAdmin):
    list_display = ('controlled_substance_stock_assignment_id', 'controlled_substance_stock',
                    'controlled_substance_stock_assignment_status')
    list_filter = ('controlled_substance_stock', 'controlled_substance_stock_assignment_status')
    ordering = ('dt_added',)
    filter_horizontal = ()


admin.site.register(StockAssignment, StockAssignmentAdmin)
