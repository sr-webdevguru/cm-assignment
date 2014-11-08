from rest_framework import serializers

from apps.devices.models import DeviceState
from apps.devices.models import Devices
from helper_functions import construct_options
from helper_functions import replace_null


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices

    def to_representation(self, instance):
        ret = super(DeviceSerializer, self).to_representation(instance)

        device_state = ret.get('device_state')
        try:
            if device_state is not None:
                ret['device_state'] = construct_options(DeviceState, device_state)
        except:
            pass

        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DeviceSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
