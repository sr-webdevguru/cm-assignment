from rest_framework import serializers

from apps.asset.models import Assets, AssetType
from apps.resorts.serializers import LocationSerializer
from helper_functions import replace_null


class AssetTypeSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        return data

    def to_representation(self, instance):
        ret = super(AssetTypeSerializer, self).to_representation(instance)
        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(AssetTypeSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = AssetType
        exclude = ('asset_type_pk', 'asset_type_status', 'resort')


class AssetSerializer(serializers.ModelSerializer):
    asset_type = AssetTypeSerializer(fields=('asset_type_id', 'asset_type_name'))
    location = LocationSerializer(fields=('location_id', 'location_name', 'area'))

    def to_internal_value(self, data):
        data.pop('location_id', None)
        data.pop('asset_type_id', None)
        return data

    def to_representation(self, instance):
        ret = super(AssetSerializer, self).to_representation(instance)
        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(AssetSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Assets
        exclude = ('asset_pk', 'asset_status', 'resort')
