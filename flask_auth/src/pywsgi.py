from gevent import monkey
from gevent.pywsgi import WSGIServer

from app import create_app
from core.config import config

app = create_app()

monkey.patch_all()
http_server = WSGIServer((config.flask.HOST, config.flask.PORT), app)
http_server.serve_forever()
