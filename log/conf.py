# default_config = {'disable_existing_loggers': False,
#                   'version': 1,
#                   'formatters':
#                       {
#                       'default':
#                           {
#                               'format': '%(asctime)s %(threadName)s [%(levelname)s] %(name)s: %(message)s'
#                           },
#                       },
#                   'handlers':
#                       {
#                           'console':
#                               {
#                                   'class': 'logging.StreamHandler',
#                                   'stream' : 'ext://sys.stderr',
#                                   'formatter': 'default'
#                               }
#                       },
#                   'loggers':
#                       {
#                           '':
#                               {
#                                   'handlers': ['console']
#                               }
#                       }
#                   }
"""Dictionary to store logger configuration"""