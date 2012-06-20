import base64
import csv
import json
import os

import urllib3
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.custom_authentication_drf import OauthAuthentication
from apps.data_sync.models import Language
from apps.data_sync.utils import handle_uploaded_file
from apps.data_sync.utils import update_language, update_user_map, update_resort_map
from apps.routing.models import Domains


@login_required()
def upload_language_file(request):
    return render(request, template_name='file-upload/index.html')


@csrf_exempt
def receive_upload(request):
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['file'])
        with open('a.csv', 'r') as destination:
            encoded_file = base64.b64encode(destination.read())

        new_language_update = Language(language_data=encoded_file)
        new_language_update.save()
        json_file_path = os.path.join(settings.STATIC_ROOT, 'language')

        if not os.path.exists(json_file_path):
            os.makedirs(json_file_path)

        with open(os.path.join(json_file_path, 'en.json'), 'w+') as jsonfile:
            with open('a.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                data = {}
                for index, row in enumerate(reader):
                    if index > 1:
                        data.update({row[2]: row[5]})
                jsonfile.write(json.dumps(data))

        if settings.RUN_ENV != 'local':
            domains = Domains.objects.all().exclude(domain=request.get_host()).filter(is_active=True)

            for domain in domains:
                pool = urllib3.PoolManager()
                url = "https://" + domain.domain + "/api/v3/sync/"
                data = {"type": "language", "data": {"csv": encoded_file}}
                header = {"Content-Type": "application/json"}
                response = pool.urlopen('POST', url, headers=header, body=json.dumps(data))

        return HttpResponse("File has been uploaded successfully")


class DataSync(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, format=None):

        type_of_operation = request.data.get('type')

        if type_of_operation == 'language':
            update_language(request.data.get('data'))
        elif type_of_operation == 'user':
            update_user_map(request.data.get('data'), request.data.get('operation'))
        elif type_of_operation == 'resort':
            update_resort_map(request.data.get('data'))
        return Response("success")


class GetLanguageFile(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (OauthAuthentication,)

    def get(self, request, lang=None):
        lang = request.GET.get('lang', '')
        if lang == 'en_US':
            json_file_path = os.path.join(settings.STATIC_ROOT, 'language', 'en.json')
            with open(json_file_path, 'r') as destination:
                lang_data = destination.read()
            return Response(json.loads(lang_data), status=200)
        else:
            response_data = {}
            language_file = Language.objects.latest('dt_created')

            response_data['version'] = language_file.id
            response_data['csv'] = language_file.language_data

        return Response(response_data, status=200)
