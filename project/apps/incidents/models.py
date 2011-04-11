import uuid
from datetime import datetime

from django.db import models
from django_enumfield import enum
from encrypted_fields.fields import EncryptedTextField
from jsonfield.fields import JSONField

from medic52.settings.common import AUTH_USER_MODEL


class Type(enum.Enum):
    ADD = 0
    REMOVE = 1


class Gender(models.Model):
    gender_id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=140)


class IncidentStatus(models.Model):
    incident_status_id = models.AutoField(primary_key=True)
    order = models.IntegerField()
    color = models.CharField(max_length=10)
    key = models.CharField(max_length=140)

    class Meta:
        ordering = ["key"]

    def __unicode__(self):
        return self.key


class Incident(models.Model):
    incident_pk = models.AutoField(primary_key=True)
    incident_id = models.UUIDField(verbose_name="incident unique id", default=uuid.uuid4, editable=False)
    resort = models.ForeignKey('resorts.Resort')
    assigned_to = models.ForeignKey(AUTH_USER_MODEL, null=True)
    dt_created = models.DateTimeField(default=datetime.now)
    dt_modified = models.DateTimeField(auto_now=True)
    incident_json = EncryptedTextField()
    incident_status = models.ForeignKey(IncidentStatus, verbose_name="incident status")
    incident_sequence = models.IntegerField(verbose_name="sequential number for incident", default=0)

    def __unicode__(self):
        return str(self.incident_id)


class IncidentAudit(models.Model):
    audit_id = models.AutoField(primary_key=True)
    incident = models.ForeignKey(Incident)
    resort = models.ForeignKey('resorts.Resort')
    prev_assigned_to = models.ForeignKey(AUTH_USER_MODEL, related_name="incident_prev_assigned_user", default=None, null=True)
    assigned_to = models.ForeignKey(AUTH_USER_MODEL, related_name="incident_assigned_user")
    changed_by = models.ForeignKey(AUTH_USER_MODEL, related_name="incident_changed_user")
    dt_created = models.DateTimeField(auto_now_add=True)


class IncidentTemplateExceptions(models.Model):
    exception_id = models.AutoField(primary_key=True)
    resort = models.ForeignKey('resorts.Resort')
    json = JSONField()
    type = enum.EnumField(Type)
    dt_updated = models.DateTimeField(auto_now=True)


class IncidentTemplate(models.Model):
    template_id = models.AutoField(primary_key=True)
    json = JSONField()


class IncidentNotes(models.Model):
    note_id = models.AutoField(primary_key=True)
    incident = models.ForeignKey(Incident)
    note = models.TextField(verbose_name="note text", blank=True, null=True)
    note_date = models.DateTimeField(verbose_name="Date for Note creation", blank=True, null=True)
    user = models.ForeignKey(AUTH_USER_MODEL, null=True)


class StatusHistory(models.Model):
    status_history_id = models.AutoField(primary_key=True)
    incident = models.ForeignKey(Incident)
    status = models.ForeignKey(IncidentStatus)
    status_date = models.DateTimeField()
    user = models.ForeignKey(AUTH_USER_MODEL)


class Patients(models.Model):
    incident_patient_id = models.AutoField(primary_key=True)
    patient_id = models.UUIDField(default=uuid.uuid4, editable=False)
    incident = models.ForeignKey(Incident)
