#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from datetime import datetime, timezone
from typing import Dict, Optional

import jwt
from pydantic import BaseModel

_namespace: str = "https://pending.ai/claims"


def get_jwt_token_claims(token: str) -> Dict:
    """
    Extract a jwt token claims segment without verifying the token
    signature. No external http request is made to the known jwks.

    Args:
        token (str): Jwt token to decode using `jwt`.

    Raises:
        ValueError: Exception encountered decoding the jwt token.

    Returns:
        Dict: Jwt token claims.
    """
    try:
        return jwt.decode(token, options={"verify_signature": False})
    except Exception as ex:
        raise ValueError("Cannot decode invalid token.") from ex


def access_token_is_expired(token: str) -> bool:
    """
    Check if an access token has reached its expiry timestamp.

    Args:
        token (str): Access token being checked for expiration.

    Raises:
        ValueError: Exception encountered decoding the jwt token.

    Returns:
        bool: Access token is expired.
    """
    try:
        tz: timezone = timezone.utc
        expires_at: int = get_jwt_token_claims(token)["exp"]
        return datetime.fromtimestamp(expires_at, tz=tz) < datetime.now(tz=tz)
    except Exception as ex:
        raise ValueError("Cannot decode invalid token.") from ex


class AccessToken(BaseModel):
    """
    Access token abstraction as received from Auth0 using the device
    authorization code or refresh token flows with `/oauth/token`.
    Helper methods are defined for checking if the token is expired or
    to extract additional jwt claims.
    """

    access_token: str
    refresh_token: str
    id_token: str
    token_type: str
    expires_in: int
    scope: str

    def get_email(self) -> str:
        """
        Extract the custom user email claim from the access token.

        Returns:
            str: User email claim.
        """
        return get_jwt_token_claims(self.access_token)[f"{_namespace}/email"]

    def get_account_type(self) -> str:
        """
        Extract the custom account type claim from the access token.

        Returns:
            str: Account type claim.
        """
        return get_jwt_token_claims(self.access_token)[f"{_namespace}/account_type"]

    def get_org_id(self) -> Optional[str]:
        """
        Extract the custom org id claim from the access token.

        Returns:
            str: Org id claim.
        """
        return get_jwt_token_claims(self.access_token).get(f"{_namespace}/org_id")

    def get_org_name(self) -> Optional[str]:
        """
        Extract the custom org name claim from the access token.

        Returns:
            str: Org name claim.
        """
        return get_jwt_token_claims(self.access_token).get(f"{_namespace}/org_name")

    def is_expired(self) -> bool:
        """
        Check if the access_token has expired.

        Returns:
            bool: _description_
        """
        return access_token_is_expired(self.access_token)
