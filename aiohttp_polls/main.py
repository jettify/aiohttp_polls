
import asyncio
import pathlib

import aiohttp_jinja2
import jinja2
from aiohttp import web

from aiohttp_polls.views import SiteHandler
from aiohttp_polls.utils import init_postgres, load_config
from aiohttp_polls.routes import setup_routes


PROJ_ROOT = pathlib.Path(__file__).parent.parent
TEMPLATES_ROOT = pathlib.Path(__file__).parent / 'templates'


async def init(loop):
    app = web.Application(loop=loop)
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(str(TEMPLATES_ROOT)))
    conf = load_config(str(PROJ_ROOT / 'config' / 'polls.yaml'))
    pg = await init_postgres(conf['postgres'], loop)

    handler = SiteHandler(pg)
    setup_routes(app, handler, PROJ_ROOT)
    app_handler = app.make_handler()

    host, port = conf['host'], conf['port']
    srv = await loop.create_server(app_handler, host, port)
    print("Server started at http://{0}:{1}".format(host, port))
    return srv, app_handler


loop = asyncio.get_event_loop()
srv, app_handler = loop.run_until_complete(init(loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.run_until_complete(app_handler.finish_connections())
    srv.close()
    loop.run_until_complete(srv.wait_closed())
loop.close()
