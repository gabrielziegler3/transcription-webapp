import httpx


class ServerClient:
    def __init__(self, timeout=10):
        self.client = httpx.AsyncClient(timeout=timeout)

    async def post(self, **args):
        return await self.client.post(**args)

    async def get(self, **args):
        return await self.client.get(**args)


server_client = ServerClient()
