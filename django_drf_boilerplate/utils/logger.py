'''
logging configuration for django project
'''
from datetime import datetime


def get_extra_params(record):
    """Returns extra params for the logger filter that can be accessed on formatter

    Args:
        record (LogRecord): LogRecord object
    """
    record.ip = record.request.META.get('REMOTE_ADDR')  # ip
    record.time = datetime.strftime(
        datetime.now(), '%Y-%m-%d %H:%M %p')  # formatted date and time
    return True
