import datetime

import factory

from apps.custom_user.factory.user_factory import UserFactory
from apps.incidents.models import IncidentStatus, Incident
from apps.resorts.factory.resort_factory import ResortFactory


class IncidentStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IncidentStatus
        django_get_or_create = {'key', }

    incident_status_id = factory.Sequence(int)
    order = 1
    color = 'ff0000'
    key = 'call_received'


class IncidentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Incident

    resort = ResortFactory()
    assigned_to = UserFactory()
    dt_created = datetime.datetime.now()
    dt_modified = datetime.datetime.now()
    incident_status = IncidentStatusFactory()
