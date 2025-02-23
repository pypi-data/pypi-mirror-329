import traceback


def exception_to_string(e):
    return "".join(traceback.format_exception(type(e), e, e.__traceback__))
