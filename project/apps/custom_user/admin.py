from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from apps.custom_user.models import UserRoles
from apps.custom_user.models import Users


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'user_id', 'is_admin', 'user_connected', 'is_active')
    list_filter = ('is_admin', 'is_active')
    add_fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Personal info', {'fields': ('locale', 'phone')}),
        ('Permissions', {'fields': ('is_admin', 'user_asset_management', 'user_controlled_substances')}),
    )
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Personal info', {'fields': ('locale', 'phone', 'user_connected')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'user_asset_management', 'user_controlled_substances')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(Users, MyUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
admin.site.register(UserRoles)
