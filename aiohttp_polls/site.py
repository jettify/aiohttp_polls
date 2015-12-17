import asyncio
import aiohttp_jinja2
from aiohttp import web
from . import db


class SiteHandler:

    def __init__(self, pg):
        self.postgres = pg

    @aiohttp_jinja2.template('index.html')
    @asyncio.coroutine
    def index(self, request):
        with (yield from self.postgres) as conn:
            cursor = yield from conn.execute(
                db.question.select())
            records = yield from cursor.fetchall()
        questions = [dict(q) for q in records]
        return {
            'questions': questions
        }

    async def poll(self, request):
        return web.Response(body=b'Body Response')

    async def results(self, request):
        return web.Response(body=b'Body Response')

    async def vote(self, request):
        return web.Response(body=b'Body Response')
