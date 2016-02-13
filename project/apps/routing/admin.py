from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from apps.routing.models import Domains, Languages, RoutingCompany, RoutingUser


class RoutingCompanyAdmin(ModelAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('resort_name', 'resort_token', 'domain')
    list_filter = ('domain',)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    search_fields = ('resort_name',)
    ordering = ('resort_name',)
    filter_horizontal = ()


class RoutingUserAdmin(ModelAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'domain')
    list_filter = ('domain',)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Domains)
admin.site.register(RoutingCompany, RoutingCompanyAdmin)
admin.site.register(RoutingUser, RoutingUserAdmin)
admin.site.register(Languages)
