from aiohttp import web


class SiteHandler:

    async def index(self, request):
        return web.Response(body=b'Body Response')
