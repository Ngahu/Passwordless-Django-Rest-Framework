from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CertifyConfig(AppConfig):
    name = 'certify'
    verbose = _("Passwordless DRF")


