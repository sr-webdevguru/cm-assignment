import uuid

from django.db import models

from apps.resorts.models import Resort
from medic52.settings.common import AUTH_USER_MODEL


class Report(models.Model):
    report_pk = models.AutoField(primary_key=True, db_column='report_pk')
    report_id = models.UUIDField(verbose_name="report unique id", default=uuid.uuid4, editable=False,
                                 db_column='report_id')
    global_status = models.IntegerField(verbose_name="report global status", default=0, db_column='global_status')
    report_user = models.ForeignKey(AUTH_USER_MODEL, db_column='report_user')
    report_resort = models.ForeignKey(Resort, db_column='report_resort', null=True)
