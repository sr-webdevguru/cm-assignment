import ast
import re
import types
from collections import OrderedDict

import boto3
from botocore.config import Config
from django.conf import settings
from django.db import connection
from rest_framework.pagination import LimitOffsetPagination, _get_count
from rest_framework.response import Response


def merge(x, y):
    """
    Merges two dictionary by updating only the fields in the second dictionary
    :param x-Primary Dictionary:
    :param y-Secondary Dictionary:
    :return: Merged dictionary:
    """
    # store a copy of x, but overwrite with y's values where applicable
    merged = dict(x, **y)
    xkeys = x.keys()

    # if the value of merged[key] was overwritten with y[key]'s value
    # then we need to put back any missing x[key] values
    for key in xkeys:
        # if this key is a dictionary, recurse
        if type(x[key]) is types.DictType and y.has_key(key):
            merged[key] = merge(x[key], y[key])

    return merged


def delete_keys_from_dict(dict_del, lst_keys):
    """
    Deletes the specified keys from dictionary
    :param dict_del:
    :param lst_keys:
    :return Resulting Dictionary:
    """
    for k in lst_keys:
        try:
            del dict_del[k]
        except KeyError:
            pass
    for v in dict_del.values():
        if isinstance(v, dict):
            delete_keys_from_dict(v, lst_keys)

    return dict_del


def replace_null(val):
    """
    Replaces the None type with empty string in the dict
    """

    for k, v in val.iteritems():
        if isinstance(v, dict):
            replace_null(v)
            continue
        if val[k] is None:
            val[k] = ""
    return val


class CustomPagination(LimitOffsetPagination):
    limit_query_param = 'chunk'
    offset_query_param = 'offset'
    max_limit = None

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('offset', self.offset),
            ('chunk', self.limit),
            ('count', self.count),
            ('results', data)
        ]))

    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None
        self.offset = self.get_offset(request)
        self.count = _get_count(queryset)

        if self.limit == 0 and self.offset == 0:
            self.limit = self.count

        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True
        return list(queryset[self.offset:self.offset + self.limit])


def construct_options(choice, selection):
    a = {}
    for item in choice:
        if item[0] == selection:
            a['key'] = item[1]
            a['value'] = item[0]
    return a


def update_reference(val, reference, path):
    replaced_string = re.subn(r"'%s'" % reference, "'%s'" % path, str(val))
    return ast.literal_eval(replaced_string[0]), replaced_string[1]


def convert_list_to_dict(val):
    final_dict = {}
    for each_dict in val:
        final_dict.update({each_dict.keys()[0]: each_dict[each_dict.keys()[0]]})
    return final_dict


# Sorting function for drug administered by
def val_for_sorting(val):
    return int(val.split(" ")[0])


def sort_drug_administered_by(val):
    with_used = []
    without_used = []
    final = []

    for each_val in val:
        if each_val[each_val.keys()[0]].startswith('USED'):
            with_used.append(each_val)
        else:
            without_used.append(each_val)

    without_used = sorted(without_used, key=lambda k: val_for_sorting(k[k.keys()[0]]))
    with_used = sorted(with_used, key=lambda k: val_for_sorting(k[k.keys()[0]].split(" ", 1)[1]))

    final = without_used + with_used

    return final


def create_client():
    return boto3.client('kms', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name=settings.AWS_REGION)


def create_s3_client():
    return boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name=settings.AWS_REGION, config=Config(signature_version='s3v4'))


def encrypt_patient_data_kms(resort, pre_data_key, new_data_key):
    from apps.incidents.models import Patients
    from apps.incidents.utils import dictfetchall
    patient_id = Patients.objects.filter(incident__resort__resort_id=resort.resort_id).values_list(
        'incident_patient_id', flat=True)

    if len(patient_id) > 0:
        cursor = connection.cursor()

        cursor.execute("""SELECT
  incident_patient_id,
  pgp_sym_decrypt(name, keys.datakey)     AS name,
  pgp_sym_decrypt(address, keys.datakey)  AS address,
  pgp_sym_decrypt(suburb, keys.datakey)   AS suburb,
  pgp_sym_decrypt(state, keys.datakey)    AS state,
  pgp_sym_decrypt(postcode, keys.datakey) AS postcode,
  pgp_sym_decrypt(phone, keys.datakey)    AS phone,
  pgp_sym_decrypt(email, keys.datakey)    AS email,
  pgp_sym_decrypt(dob, keys.datakey) AS dob
FROM incidents_patients
CROSS JOIN (SELECT %s::TEXT As datakey) As keys
    WHERE incidents_patients.incident_patient_id IN %s;""", [pre_data_key, tuple(patient_id)])

        data = dictfetchall(cursor)

        for each_data in data:
            cursor.execute("""UPDATE incidents_patients SET
                            name = pgp_sym_encrypt(v.name, keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         address = pgp_sym_encrypt(v.address, keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         suburb = pgp_sym_encrypt(v.suburb, keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         state = pgp_sym_encrypt(v.state,keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         postcode = pgp_sym_encrypt(v.postcode, keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         phone = pgp_sym_encrypt(v.phone,keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         email = pgp_sym_encrypt(v.email, keys.datakey, 'compress-algo=1, cipher-algo=aes256'),
                         dob = pgp_sym_encrypt(v.dob, keys.datakey, 'compress-algo=1, cipher-algo=aes256')
                        FROM (
                          VALUES (
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s
                          )
                            ) AS v (
                           name,
                           address,
                           suburb,
                           state,
                           postcode,
                           phone,
                           email,
                           dob
                          )
CROSS JOIN (SELECT %s::TEXT As datakey) As keys
WHERE incidents_patients.incident_patient_id = %s;""", [each_data['name'], each_data['address'],
                                                each_data['suburb'], each_data['state'], each_data['postcode'],
                                                each_data['phone'], each_data['email'],
                                                each_data['dob'], new_data_key, each_data['incident_patient_id']])

        cursor.close()

        return True


def encrypt_s3_files(resort, new_cmk):

    s3_client = create_s3_client()

    resort_media_objects = s3_client.list_objects(Bucket=settings.BUCKET_NAME, Prefix=str(resort.resort_id) + "/")

    if 'Contents' in resort_media_objects:
        for each_object in resort_media_objects['Contents']:

            try:
                each_object_file = s3_client.get_object(Bucket=settings.BUCKET_NAME, Key=each_object['Key'])
            except:
                return False, "Get file failed for " + each_object['Key']

            try:
                upload_response = s3_client.put_object(Body=each_object_file['Body'].read(), Bucket=settings.BUCKET_NAME,
                                                   Key=each_object['Key'], ServerSideEncryption="aws:kms",
                                                   SSEKMSKeyId=new_cmk)
            except:
                return False, "Upload file failed for " + each_object['Key']

        return True, ""
    else:
        return True, ""
