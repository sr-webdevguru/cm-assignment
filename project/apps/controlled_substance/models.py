import uuid

from django.db import models

from apps.incidents.models import Incident
from medic52.settings.common import AUTH_USER_MODEL
from apps.resorts.models import Resort, ResortLocation

LIVE = 0
DELETED = 1
CONTROLLED_SUBSTANCE_STATUS = (
    (LIVE, 'live'),
    (DELETED, 'deleted')
)

IN = 0
OUT = 1
USED = 2
DISPOSED = 3
STOCK_CURRENT_STATUS = (
    (IN, 'in'),
    (OUT, 'out'),
    (USED, 'used'),
    (DISPOSED, 'disposed')
)

STOCK_ASSIGNMENT_STATUS = (
    (IN, 'in'),
    (OUT, 'out'),
    (USED, 'used')
)


class ControlledSubstances(models.Model):
    controlled_substance_pk = models.AutoField(primary_key=True, db_column="controlled_substance_pk",
                                               verbose_name="controlled substance pk")
    controlled_substance_id = models.UUIDField(db_column="controlled_substance_id", default=uuid.uuid4, editable=False,
                                               verbose_name="controlled substance id")
    controlled_substance_name = models.CharField(db_column="controlled_substance_name",
                                                 verbose_name="controlled substance name", max_length=140, null=False,
                                                 blank=False)
    controlled_substance_status = models.IntegerField(db_column="controlled_substance_status",
                                                      verbose_name="controlled substance status",
                                                      choices=CONTROLLED_SUBSTANCE_STATUS, default=LIVE)
    resort = models.ForeignKey(Resort, db_column="resort", verbose_name="resort")
    units = models.CharField(db_column="units", verbose_name="units", max_length=140)

    def __str__(self):
        return self.controlled_substance_name


class Stock(models.Model):
    controlled_substance_stock_pk = models.AutoField(primary_key=True, db_column="controlled_substance_stock_pk",
                                                     verbose_name="controlled substance stock pk")
    controlled_substance_stock_id = models.UUIDField(db_column="controlled_substance_stock_id",
                                                     verbose_name="controlled substance stock id", default=uuid.uuid4,
                                                     editable=False)
    controlled_substance = models.ForeignKey(ControlledSubstances, db_column="controlled_substance",
                                             verbose_name="controlled substance id")
    location = models.ForeignKey(ResortLocation, db_column="location", verbose_name="location")
    volume = models.FloatField(db_column="volume", verbose_name="volume")
    dt_expiry = models.DateTimeField(db_column="dt_expiry", verbose_name="date of expiry", null=True, blank=True)
    dt_added = models.DateTimeField(db_column="dt_added", verbose_name="date added", auto_now_add=True)
    added_by_user = models.ForeignKey(AUTH_USER_MODEL, db_column="added_by_user", verbose_name="added by user",
                                      null=True, blank=True, related_name="added_by_user")
    dt_disposed = models.DateTimeField(db_column="dt_disposed", verbose_name="date disposed", null=True, blank=True)
    disposed_by_user = models.ForeignKey(AUTH_USER_MODEL, db_column="disposed_by_user", verbose_name="disposed by user",
                                         null=True, blank=True, related_name="disposed_by_user")
    current_status = models.IntegerField(db_column="current_status", verbose_name="current status",
                                         choices=STOCK_CURRENT_STATUS, default=IN)

    def __str__(self):
        return str(self.controlled_substance_stock_id)


class StockAssignment(models.Model):
    controlled_substance_stock_assignment_pk = models.AutoField(primary_key=True,
                                                                db_column="controlled_substance_stock_assignment_pk",
                                                                verbose_name="stock assignment pk")
    controlled_substance_stock_assignment_id = models.UUIDField(db_column="controlled_substance_stock_assignment_id",
                                                                verbose_name="stock assignment id", default=uuid.uuid4,
                                                                editable=False)
    controlled_substance_stock = models.ForeignKey(Stock, db_column="controlled_substance_stock",
                                                   verbose_name="controlled substance stock", unique=True)
    user = models.ForeignKey(AUTH_USER_MODEL, db_column="user", verbose_name="user")
    dt_added = models.DateTimeField(db_column="dt_added", verbose_name="date added", auto_now_add=True)
    controlled_substance_stock_assignment_status = models.IntegerField(
        db_column="controlled_substance_stock_assignment_status", verbose_name="stock assignment status",
        choices=STOCK_ASSIGNMENT_STATUS,
        default=IN)
    incident_id = models.ForeignKey(Incident, db_column="incident_id", verbose_name="used for incident id",
                                         null=True, blank=True)
    dt_used = models.DateTimeField(db_column="dt_used", verbose_name="date used", null=True, blank=True)

    def __str__(self):
        return str(self.controlled_substance_stock_assignment_id)


class AuditLog(models.Model):
    controlled_substance_audit_log_pk = models.AutoField(primary_key=True, db_column="controlled_substance_audit_log_pk"
                                                         , verbose_name="controlled substance audit log pk")
    controlled_substance_audit_log_id = models.UUIDField(db_column="controlled_substance_audit_log_id",
                                                         verbose_name="controlled substance audit log id",
                                                         default=uuid.uuid4, editable=False)
    log_entry = models.TextField(db_column="log_entry", verbose_name="log entry")
    dt_added = models.DateTimeField(db_column="dt_added", verbose_name="date added", auto_now_add=True)
    added_by_user = models.ForeignKey(AUTH_USER_MODEL, db_column="added_by_user", verbose_name="added by user",
                                      null=True, blank=True)
    resort = models.ForeignKey(Resort, db_column="resort", verbose_name="resort")

    def __str__(self):
        return self.log_entry
