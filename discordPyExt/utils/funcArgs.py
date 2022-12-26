
def addFuncArgs(**kwargs):
    def decorator(func):
        func.__funcargs = kwargs
        return func
    return decorator