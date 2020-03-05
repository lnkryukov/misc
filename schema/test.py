from schema import Schema, Forbidden, SchemaForbiddenKeyError

try:
    Schema(
        {
            Forbidden('test', error='TEST_ERROR'): str
        }
    ).validate(
        {
            'test': 'value'
        }
    )
except SchemaForbiddenKeyError as e:
    print(  'Auto: {}\n'
            'User: {}\n'.format(e.autos, e.errors)
    )

try:
    Schema(
        {
            Forbidden('test', error='TEST_ERROR'): str
        }
    ).validate(
        {
            'test': 'value'
        }
    )
except SchemaForbiddenKeyError as e:
    print(  'Auto: {}\n'
            'User: {}\n'.format(e.autos, e.errors)
    )