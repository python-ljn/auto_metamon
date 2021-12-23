from functools import wraps


def catch(func):
    @wraps(func)
    def _wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            print(f"catch exception: {ex}")
            raise

    return _wrap
