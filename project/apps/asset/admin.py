from django.contrib import admin

from apps.asset.models import AssetType


class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ('asset_type_name', 'asset_type_status', 'resort')
    list_filter = ('asset_type_status', 'resort')
    search_fields = ('asset_type_name',)
    ordering = ('asset_type_name',)
    filter_horizontal = ()


admin.site.register(AssetType, AssetTypeAdmin)
