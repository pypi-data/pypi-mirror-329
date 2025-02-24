''' Renaming other apps for the admin interface '''
from django.contrib.auth.apps import AuthConfig
from django.contrib.sites.apps import SitesConfig

class ContribAuth(AuthConfig):
    verbose_name = "zzz: Auth (Contrib)"

class ContribSites(SitesConfig):
    verbose_name = "zzz: Sites (Contrib)"