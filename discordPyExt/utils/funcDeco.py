import typing

class FuncExecCls:
    """
    an execution instance of a function
    """
    
    _funccls : 'FuncCls'
    kwargs : typing.Dict[str, typing.Any]   
    
    def __init__(self, funccls,*args, **kwargs) -> None:
        self._funccls = funccls
        self.args = args
        self.kwargs = kwargs
    
    def exec(self,**kwargs):
        finalKwargs = {}
        
        if self._funccls.hasArgs:
            finalKwargs[self._funccls.args] = self.args
        
        # parse self.kwargs and pop the required args   
        for arg in self._funccls.requiredArgs:
            if arg in self.kwargs:
                finalKwargs[arg] = self.kwargs.pop(arg)
            
        # paerse kwargs and pop the required args
        for arg in self._funccls.requiredArgs:
            if arg in kwargs:
                finalKwargs[arg] = kwargs.pop(arg)
                
        if self._funccls.hasKwargs:
            finalKwargs[self._funccls.kwargs] = self.kwargs
            
        return self.func(**finalKwargs)
    
    @property
    def func(self):
        return self._funccls.func
        
import inspect


class FuncCls:
    """
    a function wrapper cls that allows extension of features
    """
    
    def __init__(self, func : typing.Callable) -> None:
        """
        on init, the function is analyzed and the args are stored
        """
        self.func = func 
        # analyze function args
        args = inspect.getfullargspec(func)
        self.requiredArgs = args.args
        self.kwargs = args.varkw
        self.args = args.varargs

    @property
    def hasArgs(self):
        return self.args is not None
    
    @property
    def hasKwargs(self):
        return self.kwargs is not None


    @classmethod
    def create(cls):
        def decorator(func):
            return cls(func)
        
        return decorator
    
    def __call__(self, *args, **kwargs):
        return FuncExecCls(self, *args,**kwargs)

def batch(
    *args : typing.List[FuncExecCls],
    suppress_error : bool = False,
    **kwargs,     
):
    if len(args) == 0:
        # FuncExecCls passed in as kwargs
        argKeys = [k for k,v in kwargs.items() if isinstance(v, FuncExecCls)]
        args = [v for v in kwargs.values() if isinstance(v, FuncExecCls)]
        kwargs = {k:v for k,v in kwargs.items() if not isinstance(v, FuncExecCls)}
        
        
    res = []
    
    
    for funcexec in args:
        if not isinstance(funcexec, FuncExecCls):
            raise TypeError(f"funccls must be FuncExecCls, not {type(funcexec)}")
        
        funcexec : FuncExecCls
        
        try:
            res.append(funcexec.exec(**kwargs))
        except Exception as e:
            if not suppress_error:
                raise e
            else:
                res.append(e)
                
        del funcexec
        
    if "argKeys" in locals():
        return dict(zip(argKeys, res))
        
    return res

def match(
    *args : typing.List[FuncExecCls],
    suppress_error : bool = False,
    match_method : typing.Callable = lambda x: x is not None and x is not False,
    **kwargs,
):
    counter = 0
    for funcexec in args:
        if not isinstance(funcexec, FuncExecCls):
            raise TypeError(f"funccls must be FuncExecCls, not {type(funcexec)}")
        
        funcexec : FuncExecCls
    
        try:
            val = funcexec.exec(**kwargs)
            if match_method(val):
                return counter            
        except Exception as e:
            if not suppress_error:
                raise e
            else:
                continue
            
        counter += 1
        
    return None
