import sys
import logging

DEFAULT_FORMAT = '%(asctime)s %(process)d %(processName)s %(levelname)s %(message)s - %(name)s'


class ForwardToStdErr:
    def write(self, s):
        sys.stderr.write(s)

    def isatty(self):
        return sys.stderr.isatty()

    def flush(self):
        sys.stderr.flush()

    def __getattr__(self, name):
        return sys.stderr.__getattribute__(name)


def init_logger(log_level=logging.DEBUG, logline_format=DEFAULT_FORMAT):
    logging.basicConfig(level=log_level)
    logging.captureWarnings(True)
    rootLogger = logging.getLogger()

    # create formatter
    formatter = logging.Formatter(logline_format)

    # create console handler
    streamHandler = logging.StreamHandler(ForwardToStdErr())
    streamHandler.setLevel(log_level)
    streamHandler.setFormatter(formatter)

    rootLogger.handlers = [streamHandler]

    # disable urllib3 logging statements
    logging.getLogger('urllib3').setLevel(logging.WARNING)
