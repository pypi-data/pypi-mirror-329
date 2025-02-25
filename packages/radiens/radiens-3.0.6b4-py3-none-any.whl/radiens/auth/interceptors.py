import getpass
import json
import platform
import re
import subprocess
import sys
from pathlib import Path

import boto3
import botocore.exceptions
import radiens.utils.config as cfg
from grpc_interceptor import ClientCallDetails, ClientInterceptor


class MetadataClientInterceptor(ClientInterceptor):
    def __init__(self, id_token=None, device_uuid=None):
        self._id_token = id_token
        self._device_uuid = device_uuid

    def intercept(self, method, request, call_details):
        authorization = None
        if self._id_token is not None:
            authorization = f"Bearer {self._id_token}"
        elif self._device_uuid is not None:
            authorization = f"deviceUUID {self._device_uuid}"

        # replace the authorization metadata if it exists
        new_metadata = list(
            call_details.metadata) if call_details.metadata else []
        new_metadata = [(key, value) for key,
                        value in new_metadata if key.lower() != "authorization"]
        new_metadata.append(("authorization", authorization))

        new_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            new_metadata,
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression,
        )

        return method(request, new_details)


def get_hardware_uuid() -> str:
    """Retrieve the hardware UUID for macOS, Windows, and Linux."""
    system = platform.system()

    if system == "Darwin":
        return get_macos_hardware_uuid()
    elif system == "Windows":
        return get_windows_hardware_uuid()
    elif system == "Linux":
        return get_linux_hardware_uuid()
    else:
        print(f"Unsupported OS: {system}", file=sys.stderr)
        return ""


def get_macos_hardware_uuid() -> str:
    """Retrieve the hardware UUID on macOS."""
    try:
        output = subprocess.check_output(
            ["ioreg", "-d2", "-c", "IOPlatformExpertDevice"], encoding="utf-8"
        )
    except subprocess.CalledProcessError as e:
        print("Failed to run ioreg:", e, file=sys.stderr)
        return ""

    match = re.search(r'"IOPlatformUUID"\s=\s"([^"]+)"', output)
    return match.group(1) if match else ""


def get_windows_hardware_uuid() -> str:
    """Retrieve the hardware UUID on Windows."""
    try:
        output = subprocess.check_output(
            ["wmic", "csproduct", "get", "UUID"], encoding="utf-8"
        ).strip().split("\n")
        return output[1].strip() if len(output) > 1 else ""
    except subprocess.CalledProcessError as e:
        print("Failed to run WMIC:", e, file=sys.stderr)
        return ""


def get_linux_hardware_uuid() -> str:
    """Retrieve the hardware UUID on Linux."""
    try:
        with open("/sys/class/dmi/id/product_uuid", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        try:
            output = subprocess.check_output(
                ["dmidecode", "-s", "system-uuid"], encoding="utf-8"
            ).strip()
            return output
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print("Failed to retrieve hardware UUID on Linux:", e, file=sys.stderr)
            return ""


class SessionMetaData():
    def __init__(self):
        self._id_token = None
        self._hardware_uid = None
        app_dir = cfg.get_user_app_data_dir()
        client_id = cfg.get_app_client_id()
        refresh_token, device_key = load_session(client_id, app_dir)
        try:
            self._id_token = get_id_token(refresh_token, device_key)
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError):
            self._hardware_uid = get_macos_hardware_uuid()


# ====== helpers ======
def get_id_token(refresh_token, device_key):
    if refresh_token is None or device_key is None:
        return get_id_token_password()
    if refresh_token is not None and device_key is not None:
        return get_id_token_refresh(refresh_token, device_key)
    return None


def get_id_token_refresh(refresh_token, device_key):
    client = boto3.client('cognito-idp', region_name=cfg.REGION)
    auth_resp = client.initiate_auth(
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={
            'REFRESH_TOKEN': refresh_token,
            'DEVICE_KEY': device_key
        },
        ClientId=cfg.get_app_client_id()
    )

    client.close()
    return auth_resp['AuthenticationResult']['IdToken']


def get_id_token_password():
    _email = input('Enter user email address: ')
    _password = getpass.getpass(prompt='Enter use password: ')

    client = boto3.client('cognito-idp', region_name=cfg.REGION)
    auth_resp = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': _email,
            'PASSWORD': _password
        },
        ClientId=cfg.get_app_client_id()
    )
    client.close()

    return auth_resp['AuthenticationResult']['IdToken']


def load_session(client_id, app_dir):
    file = Path(app_dir, "session.json")
    if not file.is_file() or file.stat().st_size == 0:
        return None, None
    with open(file) as fid:
        session_info = json.load(fid)
        if 'CognitoIdentityServiceProvider' in session_info.keys():
            session_info = session_info['CognitoIdentityServiceProvider']
        else:
            return None, None
    refresh_token, device_key = (None, None)
    for _client_id, _app_client in session_info.items():
        if _client_id == client_id:
            if 'LastAuthUser' in _app_client.keys():
                user_key = _app_client['LastAuthUser']
                user_body = _app_client[user_key]
                fields = user_body.keys()
                refresh_token = user_body['refreshToken'] if 'refreshToken' in fields else None
                device_key = user_body['deviceKey'] if 'deviceKey' in fields else None

                break

    return refresh_token, device_key
