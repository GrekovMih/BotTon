# -*- encoding: utf-8 -*-
import threading
from time import time

from aioredis import create_redis_pool

import settings
from app.state.state import State
from utils.json_utils import json
from utils.thread_local import get_thread_local_loop

__all__ = (
    'StatesCache',
    'cache_state',
    'get_cached_state',
)


class StatesCache:
    pool = None

    async def run(self, loop):
        self.pool = await create_redis_pool(
            loop=loop,
            **settings.STATES_CACHE,
        )

    async def acquire(self):
        assert self.pool is not None
        return self.pool

    async def get(self, sid):
        storage = await self.acquire()
        cached = await storage.get(sid)

        if cached is None:
            return State()

        state = json.loads(cached)['state']
        return State.from_dict(state)

    async def save(self, sid, state):
        assert isinstance(state, State)

        data = json.dumps({
            'state': state.to_dict(),
        })

        storage = await self.acquire()
        await storage.set(sid, data, expire=int(time()) + settings.STATES_CACHE_TTL)


thread_local = threading.local()


async def get_cache():
    cache = getattr(thread_local, 'cache', None)

    if cache is None:
        cache = StatesCache()
        await cache.run(get_thread_local_loop())
        setattr(thread_local, 'cache', cache)

    return cache


async def cache_state(chat_id, state):
    cache = await get_cache()
    await cache.save(chat_id, state)


async def get_cached_state(chat_id):
    cache = await get_cache()
    return await cache.get(chat_id)
