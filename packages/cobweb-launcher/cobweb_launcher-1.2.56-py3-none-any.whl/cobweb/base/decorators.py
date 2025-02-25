from functools import wraps


# def check_redis_status(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         try:
#             result = func(*args, **kwargs)
#         except Exception:
#             result = False
#         return result
#
#     return wrapper


def decorator_oss_db(exception, retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(callback_func, *args, **kwargs):
            result = None
            for i in range(retries):
                msg = None
                try:
                    return func(callback_func, *args, **kwargs)
                except Exception as e:
                    result = None
                    msg = e
                finally:
                    if result:
                        return result

                    if i >= 2 and msg:
                        raise exception(msg)

        return wrapper

    return decorator



