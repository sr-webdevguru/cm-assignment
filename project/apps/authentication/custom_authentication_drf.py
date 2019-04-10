"""
Provides various authentication policies.
"""
from __future__ import unicode_literals

from django.middleware.csrf import CsrfViewMiddleware
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, HTTP_HEADER_ENCODING
from rest_framework.authtoken.models import Token

from oauth2_provider.oauth2_backends import get_oauthlib_core

OAuthLibCore = get_oauthlib_core()


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_TOKEN', b'')
    if isinstance(auth, type('')):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class BaseAuthentication(object):
    """
    All authentication classes should extend BaseAuthentication.
    """

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        raise NotImplementedError(".authenticate() must be overridden.")

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass


class TokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    model = Token
    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.select_related('user').get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (token.user, token)

    def authenticate_header(self, request):
        return 'Token'


def get_header_oauth(request):
    """
    Return request's 'Authorization:' header, as a string.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    return auth


class OauthAuthentication(BaseAuthentication):
    """
    Simple oauth based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Bearer ".  For example:

        Authorization: bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """

    def authenticate(self, request):
        access_token = get_header_oauth(request).split()

        if len(access_token) <= 1:
            msg = _('Invalid token header. No access token provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(access_token) > 2:
            msg = _('Invalid access token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        oauthlib_core = get_oauthlib_core()
        valid, r = oauthlib_core.verify_request(request, scopes=[])

        if not valid:
            raise exceptions.AuthenticationFailed(_('Invalid token (or) token has expired'))

        return None

    def authenticate_header(self, request):
        return 'Bearer'


class SessionAuthentication(BaseAuthentication):
    """
    Use Django's session framework for authentication.
    """

    def authenticate(self, request):
        """
        Returns a `User` if the request session currently has a logged in user.
        Otherwise returns `None`.
        """

        # Get the underlying HttpRequest object
        request = request._request
        user = getattr(request, 'user', None)

        # Unauthenticated, CSRF validation not required
        if not user or not user.is_active:
            return None

        # CSRF passed with authenticated user
        return (user, None)
