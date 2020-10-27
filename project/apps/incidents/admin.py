from django.contrib import admin

from apps.incidents.models import Gender, IncidentStatus, Incident, IncidentAudit, IncidentTemplateExceptions, \
    IncidentTemplate, IncidentNotes, StatusHistory
from apps.incidents.models import Patients
from helper_functions import merge, delete_keys_from_dict


class IncidentTemplateExceptionsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        resort = obj.resort
        if obj.type == 0:
            incident_template = merge(resort.incident_template, obj.json)
        elif obj.type == 1:
            del_field_list = obj.json['fields']
            incident_template = delete_keys_from_dict(resort.incident_template, del_field_list)

        resort.incident_template = incident_template
        resort.save()
        obj.save()

    list_display = ('resort', 'type', 'dt_updated')
    list_filter = ('resort', 'type', 'dt_updated')
    search_fields = ('resort',)
    ordering = ('dt_updated',)
    filter_horizontal = ()


class IncidentAuditAdmin(admin.ModelAdmin):
    list_display = ('incident', 'resort', 'assigned_to', 'changed_by', 'dt_created')
    list_filter = ('resort', 'incident', 'dt_created')
    search_fields = ('resort', 'assigned_to', 'changed_by')
    ordering = ('dt_created',)
    filter_horizontal = ()


class IncidentNotesAdmin(admin.ModelAdmin):
    list_display = ('incident', 'note', 'note_date', 'user')
    list_filter = ('incident', 'note_date', 'user')
    search_fields = ('incident', 'note_date', 'user')
    ordering = ('note_date',)
    filter_horizontal = ()


class IncidentStatusAdmin(admin.ModelAdmin):
    list_display = ('key', 'order', 'color')
    list_filter = ('order',)
    search_fields = ('key',)
    ordering = ('order',)
    filter_horizontal = ()


class IncidentTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_id',)
    list_filter = ('template_id',)
    search_fields = ('template_id',)
    ordering = ('template_id',)
    filter_horizontal = ()


class IncidentAdmin(admin.ModelAdmin):
    list_display = (
    'incident_id', 'resort', 'assigned_to', 'dt_created', 'dt_modified', 'incident_status', 'incident_sequence')
    list_filter = ('resort', 'dt_created', 'dt_modified', 'incident_status')
    search_fields = ('resort__resort_name', 'incident_status__key', 'assigned_to__email')
    ordering = ('dt_modified',)
    filter_horizontal = ()


class StatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('incident', 'status', 'status_date', 'user')
    list_filter = ('status', 'status_date', 'user')
    search_fields = ('status', 'incident')
    ordering = ('status_date',)
    filter_horizontal = ()


class PatientsAdmin(admin.ModelAdmin):
    list_display = ('incident_id', 'incident_patient_id', 'patient_id')
    filter_horizontal = ()


admin.site.register(Gender)
admin.site.register(IncidentStatus, IncidentStatusAdmin)
admin.site.register(Incident, IncidentAdmin)
admin.site.register(IncidentAudit, IncidentAuditAdmin)
admin.site.register(IncidentTemplateExceptions, IncidentTemplateExceptionsAdmin)
admin.site.register(IncidentTemplate, IncidentTemplateAdmin)
admin.site.register(IncidentNotes, IncidentNotesAdmin)
admin.site.register(StatusHistory, StatusHistoryAdmin)
admin.site.register(Patients, PatientsAdmin)
