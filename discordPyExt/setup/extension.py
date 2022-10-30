import random
import uuid
from discordPyExt.setup.interface import DcDeployerInterface
import inspect
import typing

class DcExtensionMeta(type):
    """
    metaclass for DcExtension

    it guarantees that every DcExtension has a unique hash
    """
    
    _incremental = 0
    _unique_cls = {}
    
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        # if hash is not set, set it
        if not hasattr(new_class, "_hash") or getattr(new_class, "_hash") is None:
            new_class._hash = DcExtensionMeta._incremental
            DcExtensionMeta._incremental += 1
            
        # check if it is unique
        if new_class._hash in DcExtensionMeta._unique_cls:
            raise Exception(f"Extension with hash {new_class._hash} already exists")
        
        DcExtensionMeta._unique_cls[new_class._hash] = new_class
        return new_class

class DcExtension:
    _hash = None
    _base : DcDeployerInterface = None
        
    def __hash__(self, *args, **kwargs) -> int:
        return hash(self._hash)
    
    def check_init(self):
        """
        this function executes before init
        """
        return True
    
    def check_setup(self, *args, **kwargs):
        """
        this function executes before setup
        """
        return True
    
    def check(self, *args, **kwargs):
        """
        this function executes on check
        """
        return True

    
    def init(self, *args, **kwargs) -> None:
        """
        this function executes on load
        """
        
    def setup(self, *args, **kwargs) -> None:
        """
        this function executes on setup
        """
    
    def run(self):
        """
        this function executes on run
        """
        
    @classmethod
    def configs(cls) -> typing.Dict[str, typing.Any]:
        params_for_init : dict = dict(inspect.signature(cls.init).parameters)
        # 
        params_for_setup : dict = dict(inspect.signature(cls.setup).parameters)
    
        # merge
        params_for_init.update(params_for_setup)
        
        # exclude self
        params_for_init.pop("self", None)
        # pop args and kwargs
        params_for_init.pop("args", None)
        params_for_init.pop("kwargs", None)
        

        params = {}
        for k, v in params_for_init.items():
            if v.default is not inspect.Parameter.empty:
                params[k] = v.default
            else:
                params[k] = None
        
        return params
        
    def __setattr__(self, __name: str, __value) -> None:
        if __name.startswith("_"):
            return super().__setattr__(__name, __value)
        
        if self._base is None:
            raise AttributeError(f"base not set")
        
        self._base.storage[__name] = __value
        
    def __getattribute__(self, __name: str):
        if __name.startswith("_") or __name in ["check_init", "init", "setup", "run", "configs", "check_setup", "check"]:
            return super().__getattribute__(__name)
        
        if self._base is None:
            raise AttributeError(f"base not set")
        
        return self._base.storage[__name]
        