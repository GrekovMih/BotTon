# -*- encoding: utf-8 -*-
import asyncio
import threading

import aiohttp

__all__ = (
    'get_thread_local_loop',
    'get_thread_local_http_session',
)

thread_local = threading.local()


def get_thread_local_var(name, creator):
    value = getattr(thread_local, name, None)

    if value is None:
        value = creator()
        setattr(thread_local, name, value)

    return value


def create_loop():
    loop = None

    try:
        loop = asyncio.get_event_loop()
    except Exception:
        pass

    if loop is None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop


def get_thread_local_loop():
    return get_thread_local_var('loop', create_loop)


def get_thread_local_http_session():
    return get_thread_local_var('http_session', aiohttp.ClientSession)
