# -*- encoding: utf-8 -*-
import enum
from datetime import datetime

import settings
from utils.json_utils import json

from utils.thread_local import get_thread_local_http_session

__all__ = (
    'get_wallets_balances',
    'get_transactions',
)


def prepare_param_value(value):
    if type(value) is enum.Enum:
        return value.value

    if type(value) is dict:
        return json.dumps(_prepare_params(value))

    if type(value) is datetime:
        return value.timestamp()

    return value


def _prepare_params(params):
    return {
        key: prepare_param_value(value)
        for key, value in params.items()
        if value is not None
    }


async def get_wallets_balances(user_id, wallet_id=None):
    req = await get_thread_local_http_session().get(
        settings.CRACC_WALLETS_URL + 'wallets/balances',
        params=_prepare_params({
            'user_id': user_id,
            'wallet_id': wallet_id,
        }),
    )

    return await req.json()


async def get_transactions(user_id, count=None, page=None):
    req = await get_thread_local_http_session().get(
        settings.CRACC_WALLETS_URL + 'transactions',
        params=_prepare_params({
            'user_id': user_id,
            'count': count,
            'page': page,
        }),
    )

    return await req.json()
