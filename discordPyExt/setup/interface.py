import logging
import typing
from discordPyExt.ext.data import DataLoader
from discordPyExt.ext.storage import Storage

class DcDeployerInterface:
    path : str
    logger : logging.Logger
    extensions : typing.Dict[str, typing.Any]
    storage : Storage
    config : DataLoader
    
    @typing.overload
    def isInit(self, extension) -> bool: pass
    
    @typing.overload
    def run(self): pass
    
    @typing.overload
    def _init_extension(self, ext, _no_append : bool = False ,**parameters : typing.Dict[str, typing.Any]): pass
    
    @typing.overload
    def init(self, *extensions : typing.List): pass
    
    @typing.overload
    def setup(self, *extensions : typing.List): pass
  