from rest_framework import serializers

from apps.custom_user.serializers import UserSerializer
from apps.incidents.models import Incident
from apps.incidents.models import IncidentNotes
from apps.incidents.models import IncidentStatus
from apps.incidents.models import IncidentTemplateExceptions
from apps.incidents.models import StatusHistory
from apps.incidents.utils import get_extra_incident_info, get_patient_info, get_extra_incident_info_status_report, \
    incident_status_option_for_status_report
from apps.incidents.utils import get_incident_data
from apps.incidents.utils import incident_status_option
from apps.resorts.serializers import ResortSerializer
from helper_functions import replace_null


class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class IncidentTemplateExceptionsSerializer(serializers.ModelSerializer):
    json = JSONSerializerField()

    class Meta:
        model = IncidentTemplateExceptions

    def to_representation(self, instance):
        ret = super(IncidentTemplateExceptionsSerializer, self).to_representation(instance)
        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(IncidentTemplateExceptionsSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

# commented out for List Incident API change on 06/05/2016
# class IncidentSerializer(serializers.ModelSerializer):
#     resort = ResortSerializer(fields=('resort_id', 'resort_name'))
#     assigned_to = UserSerializer(fields=('user_id', 'name'))
#
#     class Meta:
#         model = Incident
#
#     def to_representation(self, instance):
#         config = instance.resort.incident_template
#
#         incident_json = get_incident_data(instance.incident_pk)
#
#         ret = super(IncidentSerializer, self).to_representation(instance)
#
#         data = get_extra_incident_info(config, incident_json, instance.incident_pk, 'list')
#         ret.update(data)
#
#         try:
#             ret['incident_status'] = incident_status_option(ret['incident_status'])
#         except:
#             ret['incident_status'] = ""
#
#         if instance.resort.use_sequential_incident_id == 1 and instance.assigned_to.user_connected == 1:
#             ret['incident_pk'] = instance.incident_sequence
#         else:
#             ret['incident_pk'] = instance.incident_pk
#
#         return replace_null(ret)
#
#     def __init__(self, *args, **kwargs):
#         # Don't pass the 'fields' arg up to the superclass
#         fields = kwargs.pop('fields', None)
#
#         # Instantiate the superclass normally
#         super(IncidentSerializer, self).__init__(*args, **kwargs)
#
#         if fields is not None:
#             # Drop any fields that are not specified in the `fields` argument.
#             allowed = set(fields)
#             existing = set(self.fields.keys())
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)


class IncidentListSerializer(serializers.ModelSerializer):
    resort = ResortSerializer(fields=('resort_id', 'resort_name'))
    assigned_to = UserSerializer(fields=('user_id', 'name'))

    class Meta:
        model = Incident

    def to_representation(self, instance):
        config = instance.resort.incident_template

        incident_json = get_incident_data(instance.incident_pk)

        ret = super(IncidentListSerializer, self).to_representation(instance)
        incident_status = ret['incident_status']
        ret.update(incident_json)
        data = get_extra_incident_info(config, incident_json, instance.incident_pk, 'list', self.context['data_key'])
        ret.update(data)

        ret.update(get_patient_info(instance.incident_pk, self.context['data_key']))

        try:
            ret['incident_status'] = incident_status_option(incident_status)
        except:
            ret['incident_status'] = ""

        if instance.resort.use_sequential_incident_id == 1 and instance.assigned_to.user_connected == 1:
            ret['incident_pk'] = instance.incident_sequence
        else:
            ret['incident_pk'] = instance.incident_pk


        notes = IncidentNotes.objects.filter(incident=instance).order_by('-note_date')
        ret['notes'] = IncidentNotesSerializer(notes, fields=('note_id', 'note_date', 'note', 'user'),
                                                             many=True).data

        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(IncidentListSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class IncidentReportSerializer(serializers.ModelSerializer):
    resort = ResortSerializer(fields=('resort_id', 'resort_name'))
    assigned_to = UserSerializer(fields=('user_id', 'name'))

    class Meta:
        model = Incident

    def to_representation(self, instance):
        config = instance.resort.incident_template

        incident_json = get_incident_data(instance.incident_pk)

        ret = super(IncidentReportSerializer, self).to_representation(instance)

        data = get_extra_incident_info(config, incident_json, instance.incident_pk, 'report', self.context['data_key'])
        ret.update(data)

        try:
            ret['incident_status'] = incident_status_option(ret['incident_status'])
        except:
            ret['incident_status'] = ""

        if instance.resort.use_sequential_incident_id == 1 and instance.assigned_to.user_connected == 1:
            ret['incident_pk'] = instance.incident_sequence
        else:
            ret['incident_pk'] = instance.incident_pk

        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(IncidentReportSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class IncidentStatusReportSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(fields=('user_id', 'name'))

    class Meta:
        model = Incident

    def to_representation(self, instance):
        config = instance.resort.incident_template

        incident_json = get_incident_data(instance.incident_pk)

        ret = super(IncidentStatusReportSerializer, self).to_representation(instance)

        data = get_extra_incident_info_status_report(config, incident_json)
        ret.update(data)

        try:
            ret['incident_status'] = incident_status_option_for_status_report(ret['incident_status'])
        except:
            ret['incident_status'] = ""

        if instance.resort.use_sequential_incident_id == 1 and instance.assigned_to.user_connected == 1:
            ret['incident_pk'] = instance.incident_sequence
        else:
            ret['incident_pk'] = instance.incident_pk

        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(IncidentStatusReportSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class IncidentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentStatus

    def to_representation(self, instance):
        ret = super(IncidentStatusSerializer, self).to_representation(instance)
        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(IncidentStatusSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class StatusHistorySerializer(serializers.ModelSerializer):
    status = IncidentStatusSerializer(fields=('key', 'incident_status_id'))
    user = UserSerializer(fields=('user_id', 'name'))

    class Meta:
        model = StatusHistory

    def to_representation(self, instance):
        ret = super(StatusHistorySerializer, self).to_representation(instance)
        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(StatusHistorySerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class IncidentNotesSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user_name')

    def get_user_name(self, obj):
        return obj.user.user_id

    class Meta:
        model = IncidentNotes

    def to_representation(self, instance):
        ret = super(IncidentNotesSerializer, self).to_representation(instance)
        ret = replace_null(ret)
        return_data = {
            "field_52ca448dg94ja3": ret['note'],
            "field_52ca448dg94ja4": ret['note_date']
        }

        try:
            return_data.update({"field_52ca448dg94ja5": {"key": str(ret['user']), "value": instance.user.name}})
        except:
            pass

        try:
            return_data.update({"note_id": ret['note_id']})
        except:
            pass

        return return_data

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(IncidentNotesSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
