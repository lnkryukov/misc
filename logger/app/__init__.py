
from flask import Flask, jsonify, request
from flask.logging import default_handler
from gevent.pywsgi import WSGIServer
from gevent import monkey
import logging
import logging.config

from .config import cfg

logging.config.dictConfig(cfg.LOGGING)

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    logging.info(request)
    logging.debug(request)
    logging.warn(request)
    logging.error(request)
    logging.critical(request)
    d = dict()
    d['test'] = 'test'
    d['arr'] = list(range(1, 10))
    return jsonify(d)

def run():
    monkey.patch_all(ssl=False)
    logger = logging.getLogger('gevent') if cfg.DISABLE_EXISTING_LOGGERS is False else None
    logging.debug(cfg)
    logging.debug(logger)
    http_server = WSGIServer(
        (cfg.HOST, cfg.PORT),
        app,
        log = logger,
        error_log = logger)
    http_server.serve_forever()