#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import time
import webbrowser
from abc import ABC
from typing import Any, Dict, Optional

import httpx
from pydantic import ValidationError
from rich import print
from rich.status import Status

from pendingai.auth.models import AccessToken


class _AuthenticationFlow(ABC):
    """
    Abstract authentication flow controller class. Enforces flows to use
    a single authentication domain, client ID and audience for handling
    flow API requests. Flows provide utility methods that may need to be
    called in sequence / separately with additional output.

    Args:
        domain (str): Authentication client domain.
        client_id (str): Authentication client ID within the domain.
        audience (str): Authentication client audience for the domain.
    """

    def __init__(self, domain: str, client_id: str, audience: str):
        self._domain: str = domain
        self._client_id: str = client_id
        self._audience: str = audience


class RefreshTokenFlow(_AuthenticationFlow):
    """
    Refresh token flow from Auth0 is used to re-authenticate an already
    expired access token. The `offline_access` grant is used by the API
    application and will eventually invalidate refresh tokens that have
    exceeded a usage period.

    See more: https://auth0.com/docs/secure/tokens/refresh-tokens
    """

    def refresh(self, refresh_token: str) -> Optional[AccessToken]:
        """
        Attempts to rotate a refresh token. Any error encountered yields
        a null response indicating a failed refresh flow.

        Args:
            refresh_token (str): Previously generated refresh token for
                the matching authentication domain.

        Returns:
            Optional[AccessToken]: Successfully rotated access token or
                null from a failed refresh flow.
        """
        with Status("Refreshing device access"):
            response: httpx.Response = httpx.post(
                url=f"https://{self._domain}/oauth/token",
                data={
                    "client_id": self._client_id,
                    "audience": self._audience,
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                },
            )

        if response.status_code == 200:
            return AccessToken.model_validate(response.json())
        return None


class DeviceAuthorizationFlow(_AuthenticationFlow):
    """
    Device authorization flow from Auth0 is used to authenticate a user
    from the command-line interface. Both `openid` and `offline_access` auth
    scopes are used for detailed access token data. The process requires
    explicit user input so additional stdout is given when called.

    See more: https://auth0.com/docs/get-started/authentication-and-authorization-flow/device-authorization-flow
    """

    _max_retries: int = 25

    def _generate_device_code(self) -> Dict:
        """
        Utility method for requesting and parsing the authentication
        response when generating a device authorization code. Additional
        output is given to reflect the runtime status.

        Returns:
            Dict: Response body data.
        """
        with Status("Requesting device authorization code"):
            response: httpx.Response = httpx.post(
                url=f"https://{self._domain}/oauth/device/code",
                data={
                    "client_id": self._client_id,
                    "audience": self._audience,
                    "scope": "openid profile email offline_access",
                },
            )

        if response.status_code == 200:
            print("[green]\u2713[/] Device authorization code received.")
            return response.json()
        if response.status_code >= 400:
            print("[red]\u2717 Authentication service failed unexpectedly.")
        else:
            print("[red]\u2717 Failed requesting device code, try again.")
        sys.exit(1)

    def _generate_access_token(self, device_code: str) -> Optional[AccessToken]:
        """
        Utility method for requesting the access token on authentication
        server periodic checks based on an interval device code time. An
        access code is received successfully once user is registered.

        Args:
            device_code (str): Pre-generated device authorization code.

        Returns:
            Optional[AccessToken]: Parsed access token data model when
                successfully authenticated, otherwise null.
        """
        response: httpx.Response = httpx.post(
            url=f"https://{self._domain}/oauth/token",
            data={
                "client_id": self._client_id,
                "audience": self._audience,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_code,
            },
        )

        if response.status_code == 200:
            try:
                return AccessToken.model_validate(response.json())
            except ValidationError:
                print("[red]\u2717 Unexpected session token received, try again.")

        elif response.status_code == 403:
            if response.json()["error"] == "authorization_pending":
                return None
            if response.json()["error"] == "expired_token":
                print("[red]\u2717 Session was closed by the authentication server.")

        elif response.status_code == 429:
            print("[yellow]! Too many requests received by authentication server.")

        else:
            print("[red]\u2717 Failed requesting session token, try again.")

        sys.exit(1)

    def authorize(self) -> AccessToken:
        """
        Executes the interactive device authorization flow. Generate a
        device code session with Auth0, open a webbrowser instance and
        ping repeatedly until the device has been authenticated.
        """

        # Generate device code for authorization redirect url
        device_code_data: Dict[str, Any] = self._generate_device_code()
        redirect: str = device_code_data["verification_uri_complete"]
        user_code: str = device_code_data["user_code"]
        device_code: str = device_code_data["device_code"]

        print(f"- Navigate to the url on your device: {redirect}")
        print(f"- Enter the following code: [b]{user_code}[/]")
        time.sleep(2)
        webbrowser.open_new_tab(redirect)

        # Generate access token if user has authenticated logged in
        with Status("Waiting for device authentication"):
            for _ in range(self._max_retries):
                token: Optional[AccessToken] = self._generate_access_token(device_code)
                if token is not None:
                    return token
                time.sleep(device_code_data["interval"])

        # Capture authentication timeout on max retries
        print("[red]\u2717 Authentication timed out, try again.")
        sys.exit(1)
