# -*- encoding: utf-8 -*-
from cracc_database.services.wallets import load_wallets

__all__ = (
    'get_wallets_list',
)


async def get_wallets_list(
        context,
        filters=None,
        fields=None,
        *args,
        **kwargs,
):
    wallets = await load_wallets(
        context.user, context.db_session,
        filters=filters,
        fields=fields,
        *args,
        **kwargs,
    )
    return wallets
