#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
from enum import Enum, unique
from typing import Callable, Dict, Optional
from urllib.parse import urljoin

from httpx import Client as HttpxClient, ConnectError, ConnectTimeout, Response
from rich import print


@unique
class _StatusCode(int, Enum):
    """
    Mapping of status code values. Status codes match expected values
    but relate to response codes from the api gateway service from aws.
    """

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    ACCESS_DENIED = 403
    NOT_FOUND = 404
    PAYLOAD_TOO_LARGE = 413
    UNSUPPORTED_MEDIA_TYPE = 415
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    TIMEOUT = 504


class Client:
    """
    App httpx client wrapper for controlling requests to service apis.
    Method overloaded functions have explicit error handling to exit
    app logic gracefully.

    Args:
        domain (str): Authentication domain url.
        subdomain (str): Application service subdomain url path extenion
            from domain parameter.
        token (str, optional): Authentication access token for target
            domain and application audience.
    """

    _timeout: int = 10

    def __init__(self, *, domain: str, subdomain: str, token: Optional[str] = None):
        self._domain: str = domain
        self._subdomain: str = subdomain
        self._token: Optional[str] = token
        self._client: HttpxClient = self._setup_client()

    def __del__(self) -> None:
        """
        Closing HTTP client when the proxy client is OOM on deleted
        from memory. Reduces handing connections for repeated calls.
        """
        self._client.close()

    def _setup_client(self) -> HttpxClient:
        """
        Setup an httpx client for a base_path url with a global domain
        and specific service domain url path. An access token is added
        as a global header if provided to the client.

        Returns:
            httpx.Client: Initialised httpx client.
        """
        headers: Dict = {}
        if self._token is not None:
            headers["Authorization"] = f"Bearer {self._token}"
        base_url: str = urljoin(self._domain, self._subdomain)
        return HttpxClient(base_url=base_url, headers=headers, timeout=self._timeout)

    @staticmethod
    def _capture_request_errors(method: Callable) -> Callable:
        """
        Capture exceptions and errors that occur when interfacing with
        the client API connection.

        Args:
            method (Callable): HTTP method client function that is being
                wrapped in required error handling.

        Returns:
            Callable: Decorator method with client error handling.
        """

        def request_wrapper(*args, **kwargs) -> Response:
            try:
                skip_errors: bool = kwargs.pop("skip_errors", False)
                response: Response = method(*args, **kwargs)

                # Capture known status code errors from the response
                # when it returns expectedly, only return if none of the
                # known codes are received.

                if skip_errors:
                    return response
                if response.status_code == _StatusCode.BAD_REQUEST:
                    print(
                        "[red]\u2717 (400)",
                        "[red]Request parameters are invalid, contact support for more",
                        "[red]information or see service documentation.",
                    )
                elif response.status_code == _StatusCode.UNAUTHORIZED:
                    print(
                        "[red]\u2717 (401)",
                        "[red]Unauthorized access, try re-authenticating by logging out",
                        "[red]or contact support for more information.",
                    )
                elif response.status_code == _StatusCode.ACCESS_DENIED:
                    if "customer_not_subscribed" in response.content.decode():
                        print(
                            "[red]\u2717",
                            "[red]You are not subscribed to this service, contact the",
                            "[red]Pending AI support team to sign up now.",
                        )
                    else:
                        print(
                            "[red]\u2717 (403)",
                            "[red]Access denied for the service, try logging out or",
                            "[red]contact support for more information.",
                        )
                elif response.status_code == _StatusCode.NOT_FOUND:
                    print(
                        "[red]\u2717 (404)",
                        "[red]Server resource not found or is unavailable, contact",
                        "[red]support for more information.",
                    )
                elif response.status_code == _StatusCode.PAYLOAD_TOO_LARGE:
                    print(
                        "[red]\u2717 (413)",
                        "[red]Payload too large, reduce size of the request or",
                        "[red]contact support for more information.",
                    )
                elif response.status_code == _StatusCode.UNSUPPORTED_MEDIA_TYPE:
                    print(
                        "[red]\u2717 (415)",
                        "[red]Server received an unsupported media type, check your",
                        "[red]request or contact support for more information.",
                    )
                elif response.status_code == _StatusCode.TOO_MANY_REQUESTS:
                    print(
                        "[red]\u2717 (429)",
                        "[red]Server received too many requests, reduce frequency of",
                        "[red]requests or contact support for more information.",
                    )
                elif response.status_code == _StatusCode.INTERNAL_SERVER_ERROR:
                    print(
                        "[red]\u2717 (500)",
                        "[red]Server error encountered, try again shortly or contact",
                        "[red]support for more information.",
                    )
                elif response.status_code == _StatusCode.TIMEOUT:
                    print(
                        "[red]\u2717 (504)",
                        "[red]Server timed out, try again shortly or contact support",
                        "[red]for more information.",
                    )
                else:
                    return response

            # Exception handling for client connection errors during
            # initial setup, or capture other unexpected runtime errors.

            except ConnectError:
                print(
                    "[red]\u2717 (501)",
                    "[red]Connection failed, try again shortly or contact support",
                    "[red]for more information.",
                )
            except ConnectTimeout:
                print(
                    "[red]\u2717 (502)",
                    "[red]Connection timed out, try again shortly or contact support",
                    "[red]for more information.",
                )
            except Exception:
                print(
                    "[red]\u2717 (503)",
                    "[red]Server failed unexpectedly, try again shortly or contact",
                    "[red]support for more information.",
                )

            # Exit application since client failed to respond

            sys.exit(1)

        return request_wrapper

    @_capture_request_errors
    def get(self, *args, **kwargs) -> Response:
        """
        Client method wrapper for making a `GET` request.

        Returns:
            Response: Error-handling HTTP response.
        """
        return self._client.get(*args, **kwargs)

    @_capture_request_errors
    def post(self, *args, **kwargs) -> Response:
        """
        Client method wrapper for making a `POST` request.

        Returns:
            Response: Error-handling HTTP response.
        """
        return self._client.post(*args, **kwargs)

    @_capture_request_errors
    def patch(self, *args, **kwargs) -> Response:
        """
        Client method wrapper for making a `PATCH` request.

        Returns:
            Response: Error-handling HTTP response.
        """
        return self._client.patch(*args, **kwargs)

    @_capture_request_errors
    def put(self, *args, **kwargs) -> Response:
        """
        Client method wrapper for making a `PUT` request.

        Returns:
            Response: Error-handling HTTP response.
        """
        return self._client.put(*args, **kwargs)

    @_capture_request_errors
    def delete(self, *args, **kwargs) -> Response:
        """
        Client method wrapper for making a `DELETE` request.

        Returns:
            Response: Error-handling HTTP response.
        """
        return self._client.delete(*args, **kwargs)

    @_capture_request_errors
    def options(self, *args, **kwargs) -> Response:
        """
        Client method wrapper for making a `OPTIONS` request.

        Returns:
            Response: Error-handling HTTP response.
        """
        return self._client.options(*args, **kwargs)

    @_capture_request_errors
    def head(self, *args, **kwargs) -> Response:
        """
        Client method wrapper for making a `HEAD` request.

        Returns:
            Response: Error-handling HTTP response.
        """
        return self._client.head(*args, **kwargs)
