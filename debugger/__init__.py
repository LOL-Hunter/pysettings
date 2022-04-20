from time import time, perf_counter, sleep
import functools

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug



def functionDebugger(func=None, timer=True, startMsg=True, stopMsg=True):
    FUNCTION = func
    def outerWrapper(_func):
        nonlocal FUNCTION
        FUNCTION = _func
        return wrapper

    def wrapper(*args, **kwargs):
        print(args, kwargs, timer, startMsg, stopMsg)
        output = FUNCTION(*args)

        return output

    return outerWrapper if func is None else wrapper
if __name__ == "__main__":
    @debug
    def sum(a, b):
        return a+b


    print("real:",sum(1, 3))
