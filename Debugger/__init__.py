from time import time, perf_counter, sleep
sleep(1)
print(perf_counter())

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

@functionDebugger(timer=False)
def sum(a, b):
    return a+b


print("real:",sum(1, 3))