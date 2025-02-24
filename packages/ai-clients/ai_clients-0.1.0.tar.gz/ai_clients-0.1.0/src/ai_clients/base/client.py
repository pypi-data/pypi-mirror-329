from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import TypeVar, Generic
from urllib.parse import urljoin

from .types import ExtendBaseModel
from .errors import ExtractResponseError, RequestError
import aiohttp
import ujson

CompletionRequest = TypeVar('CompletionRequest', bound=ExtendBaseModel)
CompletionResponse = TypeVar('CompletionResponse', bound=ExtendBaseModel)


class BaseAIClient(ABC, Generic[CompletionRequest, CompletionResponse]):
    def __init__(self, base_url: str, api_key: str, session: aiohttp.ClientSession):
        self.base_url = base_url
        self.api_key = api_key
        self.session = session

    @abstractmethod
    async def chat_completion(self, message: str, **payload) -> str:
        """
        Handles chat completion requests using a plain text message.
        Ideal for straightforward scenarios where input is a simple string.
        """
        raise NotImplementedError

    @abstractmethod
    async def chat_completion_advanced(self, message: CompletionRequest, model: str, **payload) -> CompletionResponse:
        """
        Processes chat completion requests using a structured request object.
        Designed for advanced use cases requiring additional parameters or metadata.
        """
        raise NotImplementedError

    @staticmethod
    async def extract_response(response: aiohttp.ClientResponse) -> dict:
        content_type = response.headers.get('Content-Type', '')

        match content_type:
            case 'application/json':
                return await response.json(loads=ujson.loads)
            case 'text/plain' | 'application/x-www-form-urlencoded':
                resp = await response.text()
                return ujson.loads(resp)
            case _:
                raise ExtractResponseError('Unexpected content type: {}'.format(content_type))

    async def _request(
        self,
        method: str,
        path: str,
        headers: dict | None = None,
        params: dict | None = None,
        *args,
        **kwargs,
    ) -> dict:
        url = urljoin(self.base_url, path)

        async with self.session.request(
            method=method, url=url, headers=headers, params=params, *args, **kwargs
        ) as resp:
            if not HTTPStatus(resp.status).is_success:
                raise RequestError('Unsuccessfully response status')
            return await self.extract_response(response=resp)
