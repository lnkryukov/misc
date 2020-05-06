from schema import Schema, Use
from datetime import date, time
import pprint

pp = pprint.PrettyPrinter().pprint

valid = None

try:
    valid = Schema(
        {
            'date': Use(date.fromisoformat, error='Invalid date format'),
            'time': Use(time.fromisoformat, error='Invalid time format')
        }
    ).validate(
        {
            'date': '2020-01-02a',
            'time': '23:59'
        }
    )

except Exception as e:
    pp(e)
    for err in e.errors:
        print('\tError: {}'.format(err))
    for err in e.autos:
        print('\tAutos: {}'.format(err))

print('Valid: {}'.format(valid))