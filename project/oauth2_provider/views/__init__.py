from .application import ApplicationRegistration, ApplicationDetail, ApplicationList, \
    ApplicationDelete, ApplicationUpdate
from .base import AuthorizationView, TokenView, RevokeTokenView
from .generic import ProtectedResourceView, ScopedProtectedResourceView, ReadWriteScopedResourceView
