import base64
import datetime
import os
from urlparse import urlparse


from helper_functions import update_reference, create_s3_client
from django.conf import settings
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.templatetags.tz import datetimeobject
from django.utils import timezone

register = Library()


@stringfilter
def parse_date(date_string, forma):
    """
    Return a datetime corresponding to date_string, parsed according to format.

    For example, to re-display a date string in another format::

        {{ "01/01/1970"|parse_date:"%m/%d/%Y"|date:"F jS, Y" }}
    """
    try:
        if date_string:
            value = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            if timezone.is_naive(value):
                default_timezone = timezone.get_default_timezone()
                value = timezone.make_aware(value, default_timezone)
            result = timezone.localtime(value, forma)
            # HACK: the convert_to_local_time flag will prevent
            #       automatic conversion of the value to local time.
            result = datetimeobject(result.year, result.month, result.day,
                                    result.hour, result.minute, result.second,
                                    result.microsecond, result.tzinfo)
            result.convert_to_local_time = False
            return result
        else:
            return ''
    except ValueError:
        return None

@register.filter(is_safe=True)
@stringfilter
def convert_image(url):
    """
    convert image url to base64 data for display
    """
    try:

        if url:

            file_key = '/'.join(url.split('/')[4:])
            client = create_s3_client()
            dir_path = os.path.join(settings.MEDIA_ROOT, 'media', 'tmp')
            file_path = os.path.join(dir_path, file_key.split('/')[-1])
            client.download_file(settings.BUCKET_NAME, file_key, file_path)
            with open(file_path, "rb") as image_file:
                file_bytes = image_file.read()
                image_file.close()
                data = base64.b64encode(file_bytes)
                data = "data:image/" + image_file.name.split('.')[-1] + ";base64," + data
            os.remove(file_path)
            return data
        else:
            return ''
    except:
        import sys
        return sys.exc_info()[0]


@stringfilter
def redirect_url(url):
    """
    creates the link with redirection
    """
    if url:
        parsed_url = urlparse(url)
        final_url = settings.SCHEME + 'app.medic52.com'

        if settings.RUN_ENV == 'dev':
            final_url = settings.SCHEME + 'app-dev.medic52.com/#/?redirect_url=' + url
        elif settings.RUN_ENV == 'staging':
            final_url = settings.SCHEME + 'app-staging.medic52.com/#/?redirect_url=' + url
        else:
            final_url = settings.SCHEME + 'app.medic52.com/#/?redirect_url=' + url
        return final_url
    else:
        return ''


@register.filter(is_safe=True)
def multiply(value, arg):
    return value * float(arg)


@register.filter(is_safe=True)
def repeater_field_value(value, arg):
    return_string = ""
    for val in value:
        for val1 in arg:
            for key, val2 in val1.iteritems():
                if val == key:
                    if not return_string:
                        return_string += val2
                    else:
                        return_string += ', ' + val2

    return return_string


register.filter(parse_date)
register.filter(convert_image)
register.filter(redirect_url)
register.filter(repeater_field_value)
