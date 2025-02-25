from aiohttp.client import ClientSession

from raphson_mp.util import urlencode


class Share:
    code: str
    _session: ClientSession

    def __init__(self, code: str, session: ClientSession):
        self.code = code
        self._session = session

    async def audio(self) -> bytes:
        async with self._session.get("/share/" + urlencode(self.code) + "/audio") as response:
            return await response.content.read()

    async def cover(self) -> bytes:
        async with self._session.get("/share/" + urlencode(self.code) + "/cover") as response:
            return await response.content.read()
