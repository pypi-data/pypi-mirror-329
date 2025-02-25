import re
import uuid
import random
from typing import Any
import string

import responses
from dbmi_client.settings import dbmi_settings

UUID_PATTERN = "[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}"
JSON_CONTENT_TYPE = "application/json"


def mock_fileservice_download_archivefile_response(
    token: str, archivefile_uuid: str = None, content: bytes = None
) -> responses.Response:
    """
    Return a mocked response from Fileservice when attempting to download
    a file.

    :param token: The Fileservice token to use.
    :type token: str
    :param archivefile_id: The archive file ID to retrieve.
    :type archivefile_id: str
    :param file_path: The file path to use as the downloaded file's contents.
    :type file_path: str
    :returns: A mocked response from the Fileservice server.
    :rtype: responses.Response
    """
    # If archivefile_uuid is not provided, pass regex for all UUIDs
    if not archivefile_uuid:
        archivefile_uuid = UUID_PATTERN
    return responses.Response(
        responses.GET,
        re.compile(rf"^{dbmi_settings.FILESERVICE_URL}/filemaster/api/file/{archivefile_uuid}/proxy/$"),
        body=content if content else "This is a test file.".encode(),
        status=200,
        content_type="application/octet-stream",
        match=[responses.matchers.header_matcher({"Authorization": f"Token {token}"})],
    )


def mock_fileservice_create_archivefile_response(token: str, archivefile_uuid: str = None) -> responses.Response:
    """
    Return a mocked response from Fileservice when attempting to create
    a new file.

    :param token: The Fileservice token to use.
    :type token: str
    :param archivefile_id: The archive file ID to use, if any.
    :type archivefile_id: str
    :returns: A mocked response from the Fileservice server.
    :rtype: responses.Response
    """
    if not archivefile_uuid:
        archivefile_uuid = str(uuid.uuid4())
    return responses.Response(
        responses.POST,
        re.compile(rf"^{dbmi_settings.FILESERVICE_URL}/filemaster/api/file/?$"),
        json={
            "uuid": archivefile_uuid,
        },
        status=201,
        content_type=JSON_CONTENT_TYPE,
        match=[responses.matchers.header_matcher({"Authorization": f"Token {token}"})],
    )


def mock_fileservice_get_archivefiles_response(
    token: str, archivefile_uuid: str, archivefile: dict[str, Any]
) -> responses.Response:
    """
    Return a mocked response from Fileservice when attempting to fetch
    files.

    :param token: The Fileservice token to use.
    :type token: str
    :param archivefile_id: The archive file ID to retrieve.
    :type archivefile_id: str
    :returns: A mocked response from the Fileservice server.
    :rtype: responses.Response
    """
    return responses.Response(
        responses.GET,
        re.compile(rf"^{dbmi_settings.FILESERVICE_URL}/filemaster/api/file/?"),
        json=[
            archivefile,
        ],
        status=200,
        content_type=JSON_CONTENT_TYPE,
        match=[
            responses.matchers.header_matcher({"Authorization": f"Token {token}"}),
            responses.matchers.query_param_matcher({"uuids": archivefile_uuid}),
        ],
    )


def mock_fileservice_get_archivefile_response(
    token: str, archivefile_uuid: str, archivefile: dict[str, Any]
) -> responses.Response:
    """
    Return a mocked response from Fileservice when attempting to fetch
    a file.

    :param token: The Fileservice token to use.
    :type token: str
    :param archivefile_id: The archive file ID to retrieve.
    :type archivefile_id: str
    :returns: A mocked response from the Fileservice server.
    :rtype: responses.Response
    """
    return responses.Response(
        responses.GET,
        re.compile(rf"^{dbmi_settings.FILESERVICE_URL}/filemaster/api/file/{archivefile_uuid}/?"),
        json=archivefile,
        status=200,
        content_type=JSON_CONTENT_TYPE,
        match=[
            responses.matchers.header_matcher({"Authorization": f"Token {token}"}),
        ],
    )


def mock_fileservice_archivefile_post_response(
    token: str, bucket: str, key: str, archivefile_uuid: str = None
) -> responses.Response:
    """
    Return a mocked response from Fileservice when attempting to create
    a new file upload to S3 via POST.

    :param token: The Fileservice token to use.
    :type token: str
    :param bucket: The name of the bucket being uploaded to.
    :type bucket: str
    :param key: The key of the file being uploaded.
    :type key: str
    :param archivefile_id: The archive file ID to retrieve.
    :type archivefile_id: str
    :returns: A mocked response from the Fileservice server.
    :rtype: responses.Response
    """
    # If archivefile_uuid is not provided, pass regex for all UUIDs
    if not archivefile_uuid:
        archivefile_uuid = UUID_PATTERN
    return responses.Response(
        responses.GET,
        re.compile(rf"^{dbmi_settings.FILESERVICE_URL}/filemaster/api/file/{archivefile_uuid}/post/?.*$"),
        json={
            "locationid": random.randint(100, 1000),
            "post": {
                "url": f"https://{bucket}.s3.amazonaws.com/{key}",
                "fields": {
                    "access-key-id": "some_access_key",
                },
            },
        },
        status=201,
        content_type=JSON_CONTENT_TYPE,
        match=[responses.matchers.header_matcher({"Authorization": f"Token {token}"})],
    )


def mock_fileservice_archivefile_download_response(
    token: str, archivefile_uuid: str, download_url: str
) -> responses.Response:
    """
    Return a mocked response from Fileservice when attempting to generate
    a download URL.

    :param token: The Fileservice token to use.
    :type token: str
    :param archivefile_id: The archive file ID to download.
    :type archivefile_id: str
    :param download_url: The URL to be returned by the response.
    :type download_url: str
    :returns: A mocked response from the Fileservice server.
    :rtype: responses.Response
    """
    # If archivefile_uuid is not provided, pass regex for all UUIDs
    if not archivefile_uuid:
        archivefile_uuid = UUID_PATTERN
    return responses.Response(
        responses.GET,
        re.compile(rf"^{dbmi_settings.FILESERVICE_URL}/filemaster/api/file/{archivefile_uuid}/download/?.*$"),
        json={
            "url": download_url,
        },
        status=201,
        content_type=JSON_CONTENT_TYPE,
        match=[responses.matchers.header_matcher({"Authorization": f"Token {token}"})],
    )


def mock_fileservice_uploaded_archivefile_response(token: str, archivefile_uuid: str = None) -> responses.Response:
    """
    Return a mocked response from Fileservice when attempting to mark a file
    as being uploaded to S3.

    :param token: The Fileservice token to use.
    :type token: str
    :param archivefile_id: The archive file ID to retrieve.
    :type archivefile_id: str
    :returns: A mocked response from the Fileservice server.
    :rtype: responses.Response
    """
    # If archivefile_uuid is not provided, pass regex for all UUIDs
    if not archivefile_uuid:
        archivefile_uuid = UUID_PATTERN
    return responses.Response(
        responses.GET,
        re.compile(rf"^{dbmi_settings.FILESERVICE_URL}/filemaster/api/file/{archivefile_uuid}/uploadcomplete.*$"),
        json={
            "uuid": str(uuid.uuid4()),
        },
        status=201,
        content_type=JSON_CONTENT_TYPE,
        match=[
            responses.matchers.header_matcher({"Authorization": f"Token {token}"}),
        ],
    )


def mock_s3_upload_response(bucket: str, key: str) -> responses.Response:
    """
    Return a mocked response from S3 when attempting to upload a file.

    :param bucket: The name of the bucket being uploaded to.
    :type bucket: str
    :param key: The key of the file being uploaded.
    :type key: str
    :returns: A mocked response from the Fileservice server.
    :rtype: responses.Response
    """
    # If archivefile_uuid is not provided, pass regex for all UUIDs
    return responses.Response(
        responses.POST,
        re.compile(rf"^https://{bucket}.s3.amazonaws.com/{key}$"),
        status=200,
        content_type="text/plain",
    )


def mock_reg_get_names_response(jwt: str, names: dict[str, dict[str, str]] = None) -> responses.Response:
    """
    Return a mocked response from DBMISVC-Reg when querying the "get_names"
    endpoint.

    :param jwt: The JWT of the calling user.
    :type jwt: str
    :param names: The names object to return, if any.
    :type names: dict[str, dict[str, str]]
    :returns: A mocked response from the Fileservice server.
    :rtype: responses.Response
    """
    if not names:
        names = {}
        for _ in range(0, random.randint(10, 100)):
            # Generate random strings
            email = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
            first_name = random.choice(string.ascii_uppercase) + "".join(
                random.choices(string.ascii_lowercase, k=random.randint(3, 10))
            )
            last_name = random.choice(string.ascii_uppercase) + "".join(
                random.choices(string.ascii_lowercase, k=random.randint(3, 10))
            )

            # Add entry
            names[email] = {
                "first_name": first_name,
                "last_name": last_name,
            }

    return responses.Response(
        responses.POST,
        re.compile(rf"^{dbmi_settings.REG_URL}/api/register/get_names/?.*$"),
        json=names,
        status=201,
        content_type=JSON_CONTENT_TYPE,
        match=[
            responses.matchers.header_matcher({"Authorization": f"JWT {jwt}"}),
        ],
    )


def mock_authz_get_permission_response(jwt: str, item: str = None, permission: str = None) -> responses.Response:
    """
    Return a mocked response from the DBMISvc Authorization server.

    :param jwt: The JWT to match for the calling user.
    :type jwt: str
    :param item: The permission item key to use (e.g. "Hypatio.project_key")
    :type item: str
    :param permission: The permission string to return, if any.
    :type permission: str
    :returns: A mocked response from the DBMISvc Authorization server.
    :rtype: responses.Response
    """
    # Set response
    if item and permission:
        results = [{"item": item, "permission": permission}]
    else:
        results = []

    # Set the Responses response
    return responses.Response(
        responses.GET,
        re.compile(rf"^{dbmi_settings.AUTHZ_URL}/user_permission/?.*$"),
        json={"results": results},
        status=200,
        match=[responses.matchers.header_matcher({"Authorization": f"JWT {jwt}"})],
    )


def mock_authz_grant_permission_response(jwt: str, email: str = None, status_code: int = 200) -> responses.Response:
    """
    Return a mocked response from AuthZ when attempting to grant a permission.

    :param jwt: The JWT to use.
    :type jwt: str
    :param email: The email of the user the permission is behind granted for.
    :type email: str
    :param status_code: The status code to use for the response.
    :type status_code: int
    :returns: A mocked response from the AuthZ server.
    :rtype: responses.Response
    """
    # Set matchers depending on arguments
    matchers = [responses.matchers.header_matcher({"Authorization": f"JWT {jwt}"})]
    if email:
        matchers.append(responses.matchers.json_params_matcher({"email": email}, strict_match=False))

    return responses.Response(
        responses.POST,
        re.compile(rf"^{dbmi_settings.AUTHZ_URL}/user_permission/create_item_view_permission_record/?$"),
        json=({"status": "success"} if status_code in range(200, 299) else {"status": "error"}),
        status=200,
        match=matchers,
    )


def mock_authz_remove_permission_response(jwt: str, email: str = None, status_code: int = 200) -> responses.Response:
    """
    Return a mocked response from AuthZ when attempting to remove a permission.

    :param jwt: The JWT to use.
    :type jwt: str
    :param email: The email of the user the permission is behind removed for.
    :type email: str
    :param status_code: The status code to use for the response.
    :type status_code: int
    :returns: A mocked response from the AuthZ server.
    :rtype: responses.Response
    """
    # Set matchers depending on arguments
    matchers = [responses.matchers.header_matcher({"Authorization": f"JWT {jwt}"})]
    if email:
        matchers.append(responses.matchers.json_params_matcher({"email": email}, strict_match=False))

    return responses.Response(
        responses.POST,
        re.compile(rf"^{dbmi_settings.AUTHZ_URL}/user_permission/remove_item_view_permission_record/?$"),
        json=({"status": "success"} if status_code in range(200, 299) else {"status": "error"}),
        status=status_code,
        match=matchers,
    )


def mock_authz_grant_registration_permission_response(
    jwt: str, email: str = None, status_code: int = 200
) -> responses.Response:
    """
    Return a mocked response from AuthZ when attempting to grant a registration permission.

    :param jwt: The JWT to use.
    :type jwt: str
    :param email: The email of the user the permission is behind granted for.
    :type email: str
    :param status_code: The status code to use for the response.
    :type status_code: int
    :returns: A mocked response from the AuthZ server.
    :rtype: responses.Response
    """
    # Set matchers depending on arguments
    matchers = [responses.matchers.header_matcher({"Authorization": f"JWT {jwt}"})]
    if email:
        matchers.append(responses.matchers.json_params_matcher({"email": email}, strict_match=False))

    return responses.Response(
        responses.POST,
        re.compile(rf"^{dbmi_settings.AUTHZ_URL}/user_permission/create_registration_permission_record/?$"),
        json=({"status": "success"} if status_code in range(200, 299) else {"status": "error"}),
        status=200,
        match=matchers,
    )
