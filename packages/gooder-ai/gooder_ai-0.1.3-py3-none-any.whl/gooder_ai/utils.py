from aiohttp import ClientSession
from webbrowser import open_new


def launch_browser(base_url: str, view_id: str):
    url = f"{base_url}{view_id}"
    open_new(url)


async def validate_config(validation_url: str, config: dict) -> dict:
    async with ClientSession() as session:
        output = None
        async with session.post(validation_url, json=config) as response:
            if response.status == 200:
                output = await response.json()
            else:
                error = await response.text()
                raise Exception(f"Validation failed with {response.status}: {error}")
        return output
