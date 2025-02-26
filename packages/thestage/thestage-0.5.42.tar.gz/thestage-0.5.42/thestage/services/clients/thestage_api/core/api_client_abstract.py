import json
from abc import ABC
from typing import Optional

import requests

from thestage.config import THESTAGE_API_URL
from thestage.exceptions.auth_exception import AuthException
from thestage.services.clients.thestage_api.core.http_client_exception import HttpClientException


class TheStageApiClientAbstract(ABC):
    def __init__(self, timeout: int, url: Optional[str] = None):
        self.__timeout = timeout
        self.__api_url = url

    def _get_host(self, ) -> str:
        return self.__api_url or THESTAGE_API_URL

    def _request(
            self,
            method: str,
            url: str,
            data: dict = None,
            query_params: dict = None,
            headers: Optional[dict] = None,
            token: Optional[str] = None,
    ):
        if not data:
            data = {}

        host = self._get_host()
        url = f'{host}{url}'

        request_headers = {
            'Content-Type': 'application/json',
        }

        if token:
            request_headers['Authorization'] = f"Bearer {token}"

        if headers:
            request_headers.update(headers)
        response = requests.request(
            method=method,
            url=url,
            json=data,
            params=query_params,
            headers=request_headers,
            timeout=self.__timeout,

        )
        return self._parse_api_response(response)

    @staticmethod
    def _parse_api_response(raw_response):
        content_type = raw_response.headers.get('content-type')
        message_error = None
        if content_type == 'application/json':
            try:
                result = raw_response.json()
                message_error = result.get('message', None)
            except json.JSONDecodeError:
                raise HttpClientException(
                    message=f"Failed to parse server response",
                    status_code=raw_response.status_code,
                )
        else:
            result = raw_response.content.text()

        if raw_response.status_code == 401:
            raise AuthException(
                message=f"Unauthorized",
            )
        elif raw_response.status_code == 403:
            raise HttpClientException(
                message=f"{message_error if message_error else 'Forbidden'} ({raw_response.status_code})",
                status_code=raw_response.status_code,
            )
        elif raw_response.status_code >= 400:
            raise HttpClientException(
                message=f"{message_error if message_error else 'Request error'} ({raw_response.status_code})",
                status_code=raw_response.status_code,
            )
        elif raw_response.status_code < 200 or raw_response.status_code > 300:
            raise HttpClientException(
                message=f"{message_error if message_error else 'Request error'} ({raw_response.status_code})",
                status_code=raw_response.status_code,
            )

        return result
