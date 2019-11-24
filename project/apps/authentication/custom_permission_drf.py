from rest_framework import permissions

from apps.resorts.models import ACTIVE
from apps.resorts.utils import get_resort_for_user, get_user_resort_map


class AssetAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        resort = get_resort_for_user(user)

        if resort.resort_asset_management and user.user_asset_management:
            return True
        else:
            return False


class ControlledSubstancesAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        resort = get_resort_for_user(user)

        if resort.resort_controlled_substances and user.user_controlled_substances:
            return True
        else:
            return False


class ResortPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        resort = get_resort_for_user(user)

        user_resor_map = get_user_resort_map(user, resort)

        if user_resor_map.user_status == ACTIVE:
            return True
        else:
            return False