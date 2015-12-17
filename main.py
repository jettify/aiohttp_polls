
import asyncio
import pathlib
import jinja2
import aiohttp_jinja2

from aiohttp import web
from aiohttp_polls.site import SiteHandler
from aiohttp_polls.utils import init_postgres, load_config


PROJ_ROOT = pathlib.Path(__file__).parent.parent
TEMPLATES_ROOT = pathlib.Path(__file__).parent / 'templates'


def setup_routes(app, handler):
    add_route = app.router.add_route
    add_route('GET', '/', handler.index)
    app.router.add_static('/static/',
                          path=str(PROJ_ROOT / 'static'))


async def init(loop):
    app = web.Application(loop=loop)
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(str(TEMPLATES_ROOT)))
    conf = load_config(str(PROJ_ROOT / 'config' / 'polls.yaml'))
    import ipdb
    ipdb.set_trace()
    app['pg'] = await init_postgres(conf['postgres'], loop)

    handler = SiteHandler()
    setup_routes(app, handler)
    app_handler = app.make_handler()
    srv = await loop.create_server(app_handler, '127.0.0.1', 8080)
    print("Server started at http://127.0.0.1:8080")
    return srv, handler


loop = asyncio.get_event_loop()
srv, handler = loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(handler.finish_connections())
