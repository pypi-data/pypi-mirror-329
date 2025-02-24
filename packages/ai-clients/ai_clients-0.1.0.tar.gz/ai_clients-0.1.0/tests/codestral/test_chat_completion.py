import aiohttp
import pytest
from aioresponses import aioresponses
from src.ai_clients.codestral.client import Codestral


@pytest.mark.asyncio
async def test_chat_completion():
    base_url = 'https://api.example.com'
    api_key = 'test_api_key'
    async with aiohttp.ClientSession() as session:
        client = Codestral(base_url, api_key, session)

        message = 'Hello, world!'
        expected_response = {
            'id': 'cmpl-e5cc70bb28c444948073e77776eb30ef',
            'object': 'chat.completion',
            'model': 'mistral-small-latest',
            'usage': {'prompt_tokens': 16, 'completion_tokens': 34, 'total_tokens': 50},
            'created': 1702256327,
            'choices': [
                {
                    'index': 0,
                    'message': {
                        'content': 'Hello, user!',
                        'tool_calls': [
                            {
                                'id': 'null',
                                'type': 'function',
                                'function': {'name': 'string', 'arguments': {}},
                                'index': 0,
                            }
                        ],
                        'prefix': False,
                        'role': 'assistant',
                    },
                    'finish_reason': 'stop',
                }
            ],
        }

        with aioresponses() as m:
            m.post(f'{base_url}/v1/chat/completions', payload=expected_response)

            response = await client.chat_completion(message)

            assert response == 'Hello, user!'
