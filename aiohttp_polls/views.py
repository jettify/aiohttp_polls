import asyncio

import aiohttp_jinja2
from aiohttp import web
from sqlalchemy import select
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

    @aiohttp_jinja2.template('detail.html')
    @asyncio.coroutine
    def poll(self, request):
        question_id = request.match_info['question_id']

        with (yield from self.postgres) as conn:
            cursor = yield from conn.execute(
                db.question.select()
                .where(db.question.c.id == question_id))
            question = yield from cursor.first()

            if not question:
                raise web.HTTPNotFound(text='No question with such id')

            cursor = yield from conn.execute(
                select([db.choice.c.id,
                        db.choice.c.choice_text])
                .where(db.choice.c.question_id == question_id)
                .order_by(db.choice.c.id))
            choices = yield from cursor.fetchall()

        return {
            'question': question,
            'choices': choices
        }

    @aiohttp_jinja2.template('results.html')
    @asyncio.coroutine
    def results(self, request):
        question_id = request.match_info['question_id']

        with (yield from self.postgres) as conn:
            cursor = yield from conn.execute(
                db.question.select()
                .where(db.question.c.id == question_id))
            question = yield from cursor.first()

            if not question:
                raise web.HTTPNotFound(text='No question with such id')

            cursor = yield from conn.execute(
                select([db.choice.c.votes,
                        db.choice.c.choice_text])
                .where(db.choice.c.question_id == question_id)
                .order_by(db.choice.c.id))
            choices = yield from cursor.fetchall()

        return {
            'question': question,
            'choices': choices
        }
        return web.Response(body=b'Body Response')

    @asyncio.coroutine
    def vote(self, request):
        question_id = int(request.match_info['question_id'])
        data = yield from request.post()
        try:
            choice_id = int(data['choice'])
        except (KeyError, TypeError, ValueError) as e:
            raise web.HTTPBadRequest(
                text='You have not specified choice value') from e

        with (yield from self.postgres) as conn:
            resp = yield from conn.execute(
                db.choice.update()
                .returning(*db.choice.c)
                .where(db.choice.c.question_id == question_id)
                .where(db.choice.c.id == choice_id)
                .values(votes=db.choice.c.votes + 1))
            record = yield from resp.fetchone()
            if not record:
                raise web.HTTPNotFound(text='No such question or choice')
        router = request.app.router
        url = router['results'].url(parts={'question_id': question_id})
        return web.HTTPFound(location=url)
