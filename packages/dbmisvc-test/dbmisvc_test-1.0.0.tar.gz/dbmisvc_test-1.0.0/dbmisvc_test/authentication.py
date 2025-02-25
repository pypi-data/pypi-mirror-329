import jwt
from datetime import datetime
from typing import Any
import json
import random
import string


class TestAuthentication(object):
    """
    A class that provides a set of methods for generating test authentication.
    """

    provider = "testauth"
    url = "https://test.auth.com/"
    client_id = None
    secret_key = None

    def __init__(self, *args, **kwargs):
        """
        Initialize an instance of TestAuthentication. Optionally accepts 'client_id' and 'secret_key' arguments
        if necessary to specify those as opposed to being randomly generated.
        """
        # Set a random string for the secret key
        self.client_id = kwargs.get(
            "client_id",
            "".join(random.choices(string.ascii_uppercase + string.digits, k=16)),
        )
        self.secret_key = kwargs.get(
            "secret_key",
            "".join(random.choices(string.ascii_uppercase + string.digits, k=32)),
        )

    def dbmisvc_client_auth_clients(self) -> str:
        """
        Export the dictionary object required by Django applications utilizing
        the 'djang-dbmi-client' authentication system.
        """
        return json.dumps(
            {
                self.client_id: {
                    "JWKS_URL": self.url,
                    "PROVIDER": self.provider,
                    "CLIENT_SECRET": self.secret_key,
                }
            }
        )

    def payload(self, first_name: str, last_name: str, email: str) -> dict[str, Any]:
        """
        Generate a payload for a JWT token.
        """
        now = datetime.now()
        return {
            "email": email,
            "clientID": self.client_id,
            "updated_at": now.isoformat(),
            "user_id": f"samlp|{email}",
            "identities": [
                {
                    "user_id": email,
                    "provider": "samlp",
                    "connection": "hms-it",
                    "isSocial": False,
                }
            ],
            "created_at": now.isoformat(),
            "user_metadata": {},
            "app_metadata": {},
            "https://hms-dbmi:auth0:com/name": {
                "name_first": first_name,
                "name_last": last_name,
            },
            "iss": "https://hms-dbmi.auth0.com/",
            "sub": f"samlp|{email}",
            "aud": self.client_id,
            "iat": int(now.timestamp()),
            "exp": int(now.timestamp()) + 3600,
        }

    def sign_jwt(self, payload: dict[str, Any]) -> str:
        """
        Sign a JWT token with the secret key.
        """
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def get_jwt(self, first_name: str, last_name: str, email: str) -> str:
        """
        Generate a JWT token for a given user.
        """
        return self.sign_jwt(self.payload(first_name, last_name, email))
