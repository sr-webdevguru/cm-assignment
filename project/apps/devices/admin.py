from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from apps.devices.models import Devices


class DeviceAdmin(ModelAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('device_id', 'device_state', 'device_user')
    list_filter = ('device_state',)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    search_fields = ('device_state',)
    ordering = ('device_state',)
    filter_horizontal = ()


admin.site.register(Devices, DeviceAdmin)
