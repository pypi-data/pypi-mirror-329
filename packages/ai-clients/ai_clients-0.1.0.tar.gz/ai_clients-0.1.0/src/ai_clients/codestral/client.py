import aiohttp

from src.ai_clients.base import BaseAIClient
from .types import (
    CompletionMessageRequest,
    CompletionResponse,
    CompletionMessage,
)


class Codestral(BaseAIClient[CompletionMessageRequest, CompletionResponse]):
    def __init__(self, base_url: str, api_key: str, session: aiohttp.ClientSession):
        super().__init__(base_url, api_key, session)

    @property
    def auth_headers(self) -> dict:
        return {'Authorization': f'Bearer {self.api_key}'}

    async def chat_completion(self, message: str, **payload) -> str:
        request = CompletionMessageRequest(
            messages=[
                CompletionMessage(role='user', content=message),
            ]
        )
        response = await self._request(
            'POST',
            '/v1/chat/completions',
            headers=self.auth_headers,
            json=request.model_dump(mode='json', exclude_none=True),
            **payload,
        )
        return CompletionResponse(**response).choices[0].message.content

    async def chat_completion_advanced(
        self, message: CompletionMessageRequest, model: str, **payload
    ) -> CompletionResponse:
        response = await self._request(
            'POST',
            '/v1/chat/completions',
            headers=self.auth_headers,
            json=message.model_dump(mode='json', exclude_none=True),
            **payload,
        )
        return CompletionResponse(**response)
