from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from apps.resorts.models import Location, Country
from apps.resorts.models import Resort
from apps.resorts.models import UserResortMap


class ResortAdmin(ModelAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('resort_name', 'resort_id', 'network_key', 'location')
    list_filter = ('domain_id', 'timezone')
    search_fields = ('resort_name',)
    ordering = ('resort_name',)
    filter_horizontal = ()
    readonly_fields = ('network_key',)


class UserResortMapAdmin(ModelAdmin):
    list_display = ('user', 'resort', 'role_id', 'user_status')
    list_filter = ('resort', 'role_id')
    search_fields = ('user__email', 'resort__resort_name')
    ordering = ('resort',)
    filter_horizontal = ()


class LocationAdmin(ModelAdmin):
    list_display = ('location_id', 'key', 'country')
    list_filter = ('country',)
    search_fields = ('key', 'country')
    ordering = ('location_id',)
    filter_horizontal = ()


class CountryAdmin(ModelAdmin):
    list_display = ('country_id', 'key')
    search_fields = ('key',)
    ordering = ('country_id',)
    filter_horizontal = ()


admin.site.register(Resort, ResortAdmin)
admin.site.register(UserResortMap, UserResortMapAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Country, CountryAdmin)
