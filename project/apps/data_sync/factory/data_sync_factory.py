import datetime

import factory

from apps.data_sync.models import Language


class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Language
        django_get_or_create = {'language_data', }

    id = 1
    language_data = 'test data'
    dt_created = datetime.datetime.now()
