from flask import Flask
import logging

logging.getLogger().setLevel(0)

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    logging.info('Requested path [{}]'.format(path))
    return "Server2: {}".format(path), 200

if __name__ == '__main__':
    app.run()
