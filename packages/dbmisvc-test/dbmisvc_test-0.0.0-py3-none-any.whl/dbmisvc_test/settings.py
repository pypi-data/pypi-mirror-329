import os

from django.core.management.utils import get_random_secret_key

from authentication import TestAuthentication


class DbmiClientSettingsPatcher:

    COMMON = {
        "SECRET_KEY": get_random_secret_key(),
        "DEBUG": "True",
        "ALLOWED_HOSTS": "*",
        "DBMI_ENV": "prod",
        "COOKIE_DOMAIN": ".dbmi.hms.harvard.edu",
        "AUTH_CLIENTS": TestAuthentication.dbmisvc_client_auth_clients(),
        "EMAIL_BACKEND": "django.core.mail.backends.locmem.EmailBackend",
        "SENTRY_DSN": "",
        "MYSQL_HOST": "",
        "MYSQL_PASSWORD": "",
    }

    def __init__(self, **kwargs):

        # Ensure common settings are patched
        kwargs.update({k: v for k, v in self.COMMON.items() if k not in kwargs})

        # Pass kwargs through to environment
        for key, value in kwargs.items():
            os.environ[key] = value
