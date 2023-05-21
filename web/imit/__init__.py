from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_login
from flask_admin import Admin
import logging, logging.handlers
import os.path
from flask_babel import Babel
from sqlalchemy import desc, asc
from sqlalchemy.orm import scoped_session, sessionmaker

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_url_path="")
app.config.from_object('imit.config')
if os.environ.get('IMIT_CONFIG') is not None:
    app.config.from_envvar('IMIT_CONFIG')
logging.basicConfig(level=app.config["LOG_LEVEL"])
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
admin = Admin(app)
babel = Babel(app, default_locale='ru')
with app.app_context():
    g.locale = app.config["BABEL_DEFAULT_LOCALE"]


# Initializing loggers: write log to file in production evirounment 
if not app.debug:
    file_handler = logging.handlers.RotatingFileHandler(app.config["LOG_FILE"], maxBytes=10000, backupCount=1)
    file_handler.setLevel(app.config["LOG_LEVEL"])
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

    loggers = [app.logger, logging.getLogger('sqlalchemy'), logging.getLogger('ldap3')]
    for logger in loggers:
        logger.addHandler(file_handler)

#@db.event.listens_for(db.session, 'after_commit')
#@app.context_processor

session_manager = scoped_session(sessionmaker(bind=db.engine))

@app.before_first_request
def inject_items_list():
    session = session_manager()
    def get_items_list():
        return models.Menu.query.order_by(asc(models.Menu.number))
    items = get_items_list()
    session.close()
    return dict(items_list = items)

import imit.models
import imit.controllers.main
import imit.controllers.admin
import imit.controllers.drafts
import imit.controllers.ads
import imit.controllers.employers
import imit.controllers.menu
import imit.controllers.menu_for_header
import imit.controllers.news
import imit.controllers.faq
