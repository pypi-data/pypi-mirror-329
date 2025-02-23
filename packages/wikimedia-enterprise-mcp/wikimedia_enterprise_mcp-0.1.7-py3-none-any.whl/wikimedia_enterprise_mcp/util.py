import traceback
import logging

log = logging.getLogger(__name__)


def exception_to_string(e):
    return "".join(traceback.format_exception(type(e), e, e.__traceback__))
