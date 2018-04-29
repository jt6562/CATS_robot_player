# coding: utf-8

import logging
from logging.config import dictConfig

adb_path = '/home/jitao/App/genymotion/tools/adb'
interval_check_ad_movie = 600

logging_config = dict(
    version=1,
    formatters={
        'f': {'format':
              '%(asctime)s %(name)-2s %(levelname)-4s %(message)s'}
    },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
    },
    loggers={
        'main': {'handlers': ['h'],
                 'level': logging.INFO},
        'rules': {'handlers': ['h'],
                 'level': logging.DEBUG}
    }
)

dictConfig(logging_config)

