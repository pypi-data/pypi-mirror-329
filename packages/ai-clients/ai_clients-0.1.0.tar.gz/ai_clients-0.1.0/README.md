# ai-clients

HTTP clients for easy integration with different AI models.

## Installation

To install the package, use pip:

```bash
pip install ai-clients
```

## Usage

Here is a simple example of how to use the `Codestral` client:

```python
import aiohttp
from ai_clients.codestral.client import Codestral
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        client = Codestral(base_url="https://api.example.com", api_key="your_api_key", session=session)
        response = await client.chat_completion("Hello, how are you?")
        print(response)

asyncio.run(main())
```

## Development

To set up the development environment, run:

```bash
python -m pip install --upgrade pip
python -m pip install uv
uv venv
source .venv/bin/activate
uv sync --all-extras
```

## Testing

To run the tests, use:

```bash
uv run pytest -vv
```
