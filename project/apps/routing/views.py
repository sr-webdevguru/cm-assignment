from django.conf import settings
from django.utils.translation import ugettext as _
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.authentication.custom_authentication_drf import OauthAuthentication
from apps.custom_user.utils import validate_email
from apps.routing.models import Domains
from apps.routing.models import RoutingCompany
from apps.routing.models import RoutingUser


@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes((OauthAuthentication,))
def discover(request):
    """
    Returns the appropriate api end point based on email, resort_token (or) resort_name
    """
    data = request.data
    default_domain = Domains.objects.get(pk=1)
    domain = None

    # If email is provided then end point is searched based on it. (first preference)
    email = data.get('email', '')
    if email:
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
            email = '@'.join([email_name, domain_part.lower()])
            if not validate_email(email):
                return Response({_("detail"): _("invalid email provided")}, status=400)
        except:
            return Response({_("detail"): _("invalid email provided")}, status=400)

        try:
            user_routing = RoutingUser.objects.filter(email=email).first()
            domain = user_routing.domain.domain
            laravel_domain = user_routing.domain.laravel_domain
        except:
            pass

    # If resort_name (or) resort_network_key provided then endpoint is searched based on it. (second preference)
    # First preference to the resort_network_key and second preference to resort_name
    if domain is None:
        if data.get('resort_network_key') is not None:
            try:
                resort_routing = RoutingCompany.objects.filter(resort_token=data.get('resort_network_key')).first()
                domain = resort_routing.domain.domain
                laravel_domain = resort_routing.domain.laravel_domain
            except:
                pass
        if data.get('resort_name') is not None and domain is None:
            try:
                resort_routing = RoutingCompany.objects.filter(resort_name=data.get('resort_name')).first()
                domain = resort_routing.domain.domain
                laravel_domain = resort_routing.domain.laravel_domain
            except:
                pass

    # If country data provided then end point is provided based on it (Third Preference)
    if domain is None:
        country = data.get('country', '').lower()
        if country in ["australia", "new zealand"]:
            domain_id = Domains.objects.get(pk=2)
            domain = domain_id.domain
            laravel_domain = domain_id.laravel_domain

    # If domain name is assigned then it s returned otherwise default US domain is returned

    if domain is not None:

        domain = Domains.objects.get(domain=domain)
        response = {
            'location': settings.SCHEME + domain.domain,
            'laravel_location': settings.SCHEME + domain.laravel_domain
        }
        return Response(response, status=200)
    else:
        response = {
            'location': settings.SCHEME + default_domain.domain,
            'laravel_location': settings.SCHEME + default_domain.laravel_domain
        }
        return Response(response, status=200)
