import pytest

from tests import T_client, get_csrf


@pytest.mark.online
async def test_share(client: T_client, track: str):
    async with client.post(
        "/share/create", json={"track": track, "csrf": await get_csrf(client)}, raise_for_status=True
    ) as response:
        response.raise_for_status()
        share_code = (await response.json())["code"]

    async with client.get("/share/" + share_code, raise_for_status=True) as response:
        pass

    async with client.get("/share/" + share_code + "/cover", raise_for_status=True) as response:
        pass

    async with client.get("/share/" + share_code + "/audio", raise_for_status=True) as response:
        pass

    async with client.get("/share/" + share_code + "/download/mp3", raise_for_status=True) as response:
        pass

    async with client.get("/share/" + share_code + "/download/original", raise_for_status=True) as response:
        pass
