from pathlib import Path

from tests import T_client


async def test_static(client: T_client):
    async with client.get("/static/img/raphson.png") as response:
        assert await response.read() == Path("raphson_mp/static/img/raphson.png").read_bytes()


async def test_player_js(client: T_client):
    async with client.get("/static/js/player.js") as response:
        data = await response.read()
        assert data.count(b"\n") > 2000
