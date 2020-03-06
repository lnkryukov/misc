from types import SimpleNamespace
import os

from pathlib import Path
from dotenv import load_dotenv
path = Path('.') / '.env'
print(path)
load_dotenv(dotenv_path=path, verbose=True)

cfg = SimpleNamespace()

levels = {
    'DISABLED': 9000,
    'CRITICAL': 50,
    'ERROR': 40,
    'WARNING': 30,
    'INFO': 20,
    'DEBUG': 10,
    'NOTSET': 0
}

if os.getenv('LOG_LEVEL'):
    try:
        cfg.LOG_LEVEL = int(os.getenv('LOG_LEVEL'))
    except:        
        try:
            cfg.LOG_LEVEL = levels[os.getenv('LOG_LEVEL')]
        except:
            cfg.LOG_LEVEL = 0
else:
    cfg.LOG_LEVEL = 0

disable_log = os.getenv('DISABLE_EXISTING_LOGGERS')
if disable_log:
    if disable_log == 'True':
        cfg.DISABLE_EXISTING_LOGGERS = True
    elif disable_log == 'False':
        cfg.DISABLE_EXISTING_LOGGERS = False
else:
    cfg.DISABLE_EXISTING_LOGGERS = False

cfg.LOGGING = { 
    'version': 1,
    'disable_existing_loggers': cfg.DISABLE_EXISTING_LOGGERS,
    'incremental': False,
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': { 
        'default': { 
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'level': cfg.LOG_LEVEL
        },
    },
    'root': {
        'handlers': ['default'],
        'level': cfg.LOG_LEVEL
    },
    'loggers': { 
        '': {  # root logger
            'handlers': ['default'],
            'propagate': True,
            'level': cfg.LOG_LEVEL
        },
    }
}

cfg.HOST = os.getenv('HOST')
cfg.PORT = int(os.getenv('PORT'))
cfg.ENV = os.getenv('ENV')