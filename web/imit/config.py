import logging

DEBUG = True
PROPAGATE_EXCEPTIONS = True
LISTEN_HOST = '0.0.0.0'
LISTEN_PORT = 5000
WTF_CSRF_ENABLED = False
SECRET_KEY = 'SKGBkb  )*ayfR df hg[* AFHoHZD:Fo H:AOSIFy sdfg'
LOG_FILE = 'logs/imit.log'
LOG_LEVEL = logging.DEBUG
LOGIN_DISABLED = False
TEMPLATES_AUTO_RELOAD = True

SQLITE_DATABASE_PATH = '/imit.db'
SQLALCHEMY_DATABASE_URI = 'sqlite://' + SQLITE_DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False

LDAP_SERVER = 'ldaps://ldap.cs.prv'
LDAP_PORT = 636
LDAP_USE_SSL = True

FILE_UPLOAD_PATH = 'imit/static/files/'

BABEL_DEFAULT_LOCALE = 'ru'
BABEL_DEFAULT_TIMEZONE = 'UTC'  # FIXME (or not)
LANGUAGES = {
    'en': 'English',
    'ru': 'Русский'
}

FAQ_FILE_NAME = "faq.json"

VK_API_KEY = ""
YANDEX_COUNTER_ID = ""
