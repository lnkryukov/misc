# misc

## Декоратор декарирующий декоратор (с перегрузкой)

`module.py`
```python

import logging

logging.basicConfig(format='%(module)s %(funcName)s() %(lineno)d: %(message)s',
                    level=0)

def first_decorator(func):

    logging.debug('First decorator')
    
    def wrapper():
        logging.debug('First decorator wrapper')
        return func()

    return wrapper
```

`main.py`
```python
import logging

logging.basicConfig(format='%(module)s %(funcName)s() %(lineno)d: %(message)s',
                    level=0)

from module import first_decorator as fd

def first_decorator(func):

    logging.debug('Second decorator')

    func = fd(func)

    def wrapper():
        logging.debug('Second decorator wrapper')
        return func()

    return wrapper


@first_decorator
def test():
    logging.debug('Test func')

test()
```
