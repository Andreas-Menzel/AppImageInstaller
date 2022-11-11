#-------------------------------------------------------------------------------
# logHandler
#
# Uses pythons logging module to return a well formatted, coloured logger.
#
# https://gist.github.com/Andreas-Menzel/773f2b5dcc22f00ccf740f0bfaf9a89a#file-loghandler-py
#-------------------------------------------------------------------------------
# @author: Andreas Menzel
# @license: MIT License
# @copyright: Copyright (c) 2022 Andreas Menzel
#-------------------------------------------------------------------------------
# version: 2022-10-09_1

import logging


DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50


class CustomFormatter(logging.Formatter):
    grey     = '\x1b[38;21m'
    blue     = '\x1b[38;5;39m'
    yellow   = '\x1b[38;5;226m'
    red      = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset    = '\x1b[0m'

    fmt = ''
    FORMATS = {}

    def __init__(self, mode = 'minimal', coloured = True):
        super().__init__()
        
        self.mode = mode
        self.coloured = coloured
        
    def update_FORMATS(self):
        if self.coloured:
            self.FORMATS = {
                DEBUG: self.grey + self.fmt + self.reset,
                INFO: self.blue + self.fmt + self.reset,
                WARNING: self.yellow + self.fmt + self.reset,
                ERROR: self.red + self.fmt + self.reset,
                CRITICAL: self.bold_red + self.fmt + self.reset
            }
        else:
            self.FORMATS = {
                DEBUG: self.fmt,
                INFO: self.fmt,
                WARNING: self.fmt,
                ERROR: self.fmt,
                CRITICAL: self.fmt
            }

    def format(self, record):
        if self.mode == 'normal':
            if record.levelno == logging.DEBUG or record.levelno == logging.INFO or \
               record.levelno == logging.WARNING:
                self.fmt = '[ {levelname} @ {asctime} ] {message}'
            else:
                self.fmt = '[ {levelname} @ {asctime} IN {name}, {threadName}, {funcName}() ] {message}'
        elif self.mode == 'extended':
            self.fmt = '[ {levelname} @ {asctime} IN {name}, {threadName}, {funcName}() ] {message}'
        else:
            # minimal
            record.levelname = record.levelname.center(8)
            self.fmt = '[ {levelname} ] {message}'

        self.update_FORMATS()
        
        log_fmt = self.FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt, style='{')

        return formatter.format(record)


# get_logger
#
# Returns a logger object.
#
# @param str    name            Name of the logger.
# @param dict   stream_logger   Configuration for stream-logging.
# @param dict   file_logger     Configuration for file-logging.
# @param str    mode            Format-mode. Available: (<default>,) 'minimal'
#
# @note stream_logger must have the following format:
#       { 'log_level': <log_level>, 'stream': <stream> }
#       If stream is None, the default logging stream will be used
# @note file_logger must have the following format:
#       { 'log_level': <log_level>, 'filename': <filename>, 'write_mode': 'w'|'a' }
#
# @return Returns the logger object.
def get_logger(name, stream_logger = None, file_logger = None, mode = None):
    logger = logging.getLogger(name)
    logger.setLevel(DEBUG)

    if not stream_logger is None:
        log_level = stream_logger['log_level']
        stream = stream_logger['stream']
        
        handler = logging.StreamHandler(stream)
        handler.setLevel(log_level)
        handler.setFormatter(CustomFormatter(mode))
        logger.addHandler(handler)
    
    if not file_logger is None:
        log_level = file_logger['log_level']
        filename = file_logger['filename']
        write_mode = file_logger['write_mode']
        
        if write_mode not in ['w', 'a']:
            write_mode = 'a'

        handler = logging.FileHandler(filename, mode=write_mode)
        handler.setLevel(log_level)
        handler.setFormatter(CustomFormatter(mode, coloured=False))
        logger.addHandler(handler)
    
    return logger


if __name__ == '__main__':
    logger = get_logger(name='main_logger',
                        stream_logger={ 'log_level': DEBUG, 'stream': None },
                        file_logger={ 'log_level': DEBUG,
                                      'filename': 'logfile.log',
                                      'write_mode': 'a' },
                        mode='extended')

    logger.debug('This is a debug message.')
    logger.info('This is an info message.')
    logger.warning('This is warning message.')
    logger.error('This is an error message.')
    logger.critical('This is a critical message.')