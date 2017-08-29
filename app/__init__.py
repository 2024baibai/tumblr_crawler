from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
#from celery import Celery,platforms
from flask_pagedown import PageDown

app = Flask(__name__)
app.config.from_object('config')

# Celery configuration
#celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
db = SQLAlchemy(app, use_native_unicode='utf8')
bootstrap = Bootstrap(app)
pagedown = PageDown(app)
# celery.conf.update(app.config)
#platforms.C_FORCE_ROOT = True

from app import views
