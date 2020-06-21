from rest_framework import serializers

from apps.routing.models import RoutingCompany
from apps.routing.models import RoutingUser
from helper_functions import replace_null


class RoutingCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutingCompany

    def to_representation(self, instance):
        ret = super(RoutingCompanySerializer, self).to_representation(instance)
        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(RoutingCompanySerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class RoutingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutingUser

    def to_representation(self, instance):
        ret = super(RoutingUserSerializer, self).to_representation(instance)
        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(RoutingUserSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
