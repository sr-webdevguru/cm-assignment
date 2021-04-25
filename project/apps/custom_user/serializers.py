from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.custom_user.models import UserConnected
from apps.custom_user.models import UserRoles
from apps.devices.models import Devices
from apps.devices.serializers import DeviceSerializer
from helper_functions import construct_options
from helper_functions import replace_null


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(UserSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)

        try:
            ret['user_connected'] = construct_options(UserConnected, ret['user_connected'])
        except:
            pass

        return replace_null(ret)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.email = instance.email.lower()
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        try:
            instance.email = instance.email.lower()
        except:
            pass
        instance.save()
        return instance

from apps.resorts.models import UserResortMap, USER_STATUS
from apps.resorts.serializers import ResortSerializer


class UserResortSerializer(serializers.ModelSerializer):

    resort = ResortSerializer(fields=('resort_id', 'resort_name'))
    user = UserSerializer(fields=('user_id', 'email', 'phone', 'name', 'user_connected', 'user_controlled_substances', 'user_asset_management'))

    class Meta:
        model = UserResortMap

    def to_representation(self, instance):
        final_representation = {}
        ret = super(UserResortSerializer, self).to_representation(instance)
        final_representation.update(ret['user'])
        final_representation.update({"resort": ret['resort']})

        try:
            devices = Devices.objects.filter(device_user=instance.user, device_state=0)
            devices_data = DeviceSerializer(devices, fields=('device_id', 'device_type', 'device_os'), many=True)
            final_representation['devices'] = devices_data.data
        except:
            final_representation['devices'] = []

        try:
            from apps.custom_user.utils import userrole_option
            final_representation['role_id'] = userrole_option(int(ret['role']))
        except:
            final_representation['role_id'] = ""

        try:
            final_representation['user_status'] = construct_options(USER_STATUS, ret['user_status'])
        except:
            final_representation['user_status'] = ""

        return replace_null(final_representation)


class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
