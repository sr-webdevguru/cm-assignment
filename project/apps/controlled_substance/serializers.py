from rest_framework import serializers

from apps.controlled_substance.models import AuditLog
from apps.controlled_substance.models import ControlledSubstances
from apps.controlled_substance.models import STOCK_ASSIGNMENT_STATUS
from apps.controlled_substance.models import Stock
from apps.controlled_substance.models import StockAssignment
from apps.custom_user.serializers import UserSerializer
from apps.resorts.serializers import LocationSerializer
from helper_functions import construct_options
from helper_functions import replace_null


class ControlledSubstancesSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        ret = super(ControlledSubstancesSerializer, self).to_internal_value(data)
        return ret

    def to_representation(self, instance):
        ret = super(ControlledSubstancesSerializer, self).to_representation(instance)
        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(ControlledSubstancesSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = ControlledSubstances
        exclude = ('resort',)


class StockSerializer(serializers.ModelSerializer):
    controlled_substance = ControlledSubstancesSerializer(
        fields=('controlled_substance_pk', 'controlled_substance_id', 'controlled_substance_name',
                'units'))
    location = LocationSerializer(fields=('location_id', 'location_name', 'map_lat', 'map_long'))
    added_by_user = UserSerializer(fields=('user_id', 'name'))
    disposed_by_user = UserSerializer(fields=('user_id', 'name'))

    def to_internal_value(self, data):
        ret = super(StockSerializer, self).to_internal_value(data)
        return ret

    def to_representation(self, instance):
        ret = super(StockSerializer, self).to_representation(instance)
        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(StockSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Stock


class AuditLogSerializer(serializers.ModelSerializer):
    added_by_user = UserSerializer(fields=('user_id', 'name'))

    def to_internal_value(self, data):
        ret = super(AuditLogSerializer, self).to_internal_value(data)
        return ret

    def to_representation(self, instance):
        ret = super(AuditLogSerializer, self).to_representation(instance)
        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(AuditLogSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = AuditLog
        exclude = ('controlled_substance_audit_log_pk', 'resort')


class StockAssignmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(fields=('user_id', 'name'))
    incident_id = serializers.StringRelatedField()

    def to_internal_value(self, data):
        ret = super(StockAssignmentSerializer, self).to_internal_value(data)
        return ret

    def to_representation(self, instance):
        ret = super(StockAssignmentSerializer, self).to_representation(instance)
        controlled_substance_stock_assignment_status = ret.get('controlled_substance_stock_assignment_status')

        if controlled_substance_stock_assignment_status is not None:
            try:
                ret['controlled_substance_stock_assignment_status'] = construct_options(STOCK_ASSIGNMENT_STATUS,
                                                                                        controlled_substance_stock_assignment_status)
            except:
                pass

        try:
            if 'incident_id' in ret:
                ret['incident_pk'] = instance.incident_id.incident_sequence if instance.incident_id.resort.use_sequential_incident_id else instance.incident_id.incident_pk
        except:
            pass

        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(StockAssignmentSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = StockAssignment


class StockReportSerializer(serializers.ModelSerializer):
    controlled_substance = ControlledSubstancesSerializer(
        fields=('controlled_substance_id', 'controlled_substance_name', 'controlled_substance_pk',
                'units'))
    location = LocationSerializer(fields=('location_id', 'location_name', 'map_lat', 'map_long'))
    added_by_user = UserSerializer(fields=('user_id', 'name'))
    disposed_by_user = UserSerializer(fields=('user_id', 'name'))

    def to_internal_value(self, data):
        ret = super(StockReportSerializer, self).to_internal_value(data)
        return ret

    def to_representation(self, instance):
        # Add assignment if its found
        assignment = StockAssignment.objects.filter(controlled_substance_stock=instance)

        if assignment:
            assignment_data = StockAssignmentSerializer(assignment[0], fields=('controlled_substance_stock_assignment_id',
                                                                            'dt_added', 'dt_used', 'user',
                                                                            'incident_id')).data
        else:
            assignment_data = {}


        ret = super(StockReportSerializer, self).to_representation(instance)
        ret['assignment'] = assignment_data
        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(StockReportSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Stock
