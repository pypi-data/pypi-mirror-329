from django.contrib.auth import get_user_model
from django.test import Client

from dbmisvc_test.authentication import TestAuthentication


class TestUser:

    def __init__(self, first_name: str = "Test", last_name: str = "User", email: str = "test_user@email.com"):
        super().__init__()

        # Assign properties
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

        # Create the user object in the database.
        self._instance = get_user_model().objects.create(email=self.email, username=self.email)
        self._jwt = TestAuthentication.get_jwt(first_name=self.first_name, last_name=self.last_name, email=self.email)

    def __getattr__(self, item):
        return getattr(self._instance, item)

    def __copy__(self):
        return TestUser(first_name=self.first_name, last_name=self.last_name, email=self.email)

    def login(self, client: Client):
        """
        Accepts a Client object and logs the test user into it.
        """
        client.cookies['DBMI_JWT'] = self._jwt
        client.force_login(self._instance)
