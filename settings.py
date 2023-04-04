# -*- encoding: utf-8 -*-

SERVER_PORT = 9003

DB_USER_NAME = 'cracc-admin'
DB_USER_PASSWORD = 'xxxxxxxxxx'
DB_HOST = 'xxxxxxx'
DB_PORT = '5432'
DB_NAME = 'cracc'
DB_URL = 'postgres://{}:{}@{}:{}/{}'.format(DB_USER_NAME, DB_USER_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SENTRY_DSN_API = ''
BOT_TOKEN = ''
BLOCKCYPHER_TOKEN = ''
TELEBOT_PROXY = ''

SITE_HOST = ''
MANDRILL_APIKEY = ''

STATES_CACHE = {
    'address': 'redis://localhost:6379/5',
    'password': '',
}
STATES_CACHE_TTL = 30 * 24 * 60 * 60

CRACC_WALLETS_URL = 'http://127.0.0.1:9004/'

try:
    from settings_private import *
except:
    pass

try:
    from settings_local import *
except:
    pass
