# -*- encoding: utf-8 -*-
import base64
import os
from _decimal import Decimal
from datetime import datetime, timedelta, timezone

from mnemonic import Mnemonic
from ton_client.client import TonlibClientFutures

__all__ = (
    'ton_create_key',
    'ton_get_address',
    'ton_get_state',
    'ton_get_balance',
    'ton_init_wallet',
    'ton_send_grams',
)

proj_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..')
keystore = os.path.join(proj_path, 'tmp')

TON_CLIENT = TonlibClientFutures(keystore=keystore)
MNEMONIC = Mnemonic("english")


def ton_create_key(private, password):
    new_key = TON_CLIENT.create_new_key(
        local_password=password,
        mnemonic=MNEMONIC.to_mnemonic(private).split(' '),
    ).result()

    return TON_CLIENT.decrypt_key(
        public_key=new_key['public_key'],
        secret=new_key['secret'],
        local_password=password,
    ).result()


def ton_get_address(public_key):
    result = TON_CLIENT.wallet_get_account_address(
        public_key=public_key,
    ).result()

    address = result['account_address']
    return address


def ton_get_state(address=None, public_key=None):
    if address is None:
        assert public_key is not None
        address = ton_get_address(public_key)

    return TON_CLIENT.raw_get_account_state(
        address=address,
    ).result()


def ton_get_balance(address):
    state = ton_get_state(address=address)
    balance = Decimal(state['balance']) / Decimal(1e9)
    return str(balance)


def ton_init_wallet(public_key, secret):
    return TON_CLIENT.wallet_init(
        public_key=public_key,
        secret=secret,
    ).result()


def ton_send_grams(public_key, secret, to_, count, valid_until=None):
    state = ton_get_state(public_key=public_key)

    if state['code'] == '':
        ton_init_wallet(public_key, secret)
        state = ton_get_state(public_key=public_key)

    assert state['code'] != ''

    seq_no = int.from_bytes(base64.b64decode(state['data'].encode('UTF-8'))[-36:-32], "big")

    if valid_until is None:
        valid_until = datetime.fromtimestamp((datetime.now() + timedelta(days=1)).timestamp(), tz=timezone.utc)

    return TON_CLIENT.wallet_send_grams(
        public_key=public_key,
        secret=secret,
        dest_address=to_,
        seq_no=seq_no,
        valid_until=valid_until,
        amount=int(count),
    ).result()
