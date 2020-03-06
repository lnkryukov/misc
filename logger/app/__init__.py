
from flask import Flask, jsonify, request
from flask.logging import default_handler
from gevent.pywsgi import WSGIServer
from gevent import monkey
import logging
import logging.config

from .config import cfg

'''
Логгирование нужно конфигурировать до создания app, иначе какой-нибудь логгер может успеть 
создаться раньше с дефольтным конфигом
'''
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
        log = logger, # Gevent хуй клал на логгеры и конфиги, поэтому ему отедльно нужно сказать, чтобы перестал это делать
        error_log = logger) # По умолчанию эта сволочь просто срет в stderr и не обращает внимание на конфиг
    http_server.serve_forever()