import datetime

from django.db import models
from django_cron import CronJobBase, Schedule

from apps.resorts.models import Resort
from oauth2_provider.models import AccessToken
from oauth2_provider.models import Application


class ResortOauthApp(models.Model):
    resort = models.ForeignKey(Resort, verbose_name='resort associated with oauth app')
    oauth_app = models.ForeignKey(Application, verbose_name='oauth application associated with resort')
    is_active = models.BooleanField(verbose_name='is application active ?', default=True)


class AccessTokenRemove(CronJobBase):
    RUN_EVERY_MINS = 300  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'authentication.AccessTokenRemove'  # a unique code

    def do(self):
        current_time = datetime.datetime.today()
        AccessToken.objects.filter(expires__lt=current_time).delete()
