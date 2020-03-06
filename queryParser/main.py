from flask import Flask, request, jsonify
from flask_caster import FlaskCaster
from schema import Schema, Optional
import pprint

pp = pprint.PrettyPrinter().pprint

app = Flask(__name__)

caster = FlaskCaster(app)
caster.ints = ['size', 'offset']

def parseOffsetSize(args):
    schema = Schema(
        {
            Optional('offset'): int,
            Optional('size'): int
        }, ignore_extra_keys=True
    )
    schema.validate(dict(args))
    return (args.get('offset'), args.get('size'))
    
def getData(offset=0, size=100):
    if offset is None:
        offset = 0
    if size is None:
        size = 100
    return list(range(offset + 1, offset + 1 + size))

@app.route('/test', methods=['GET'])
def test():
    offset, size = parseOffsetSize(request.args)
    res = dict()
    res['data'] = getData(offset, size)
    res['offset'] = offset
    res['size'] = size
    return jsonify(res)