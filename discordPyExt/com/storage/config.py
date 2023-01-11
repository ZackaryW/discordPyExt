
import os
import typing

from discordPyExt.com.storage.driver import Driver, JsonDriver, TomlDriver, PyDriver
from discordPyExt.utils.json import dump_file


class Config:
    def __init__(
        self, 
        drivers : typing.List[Driver], 
        enforceOrder : bool = True,
    ) -> None:
        self._drivers = drivers
        if enforceOrder:
            return
        
        # sort drivers by readable and writable
        self._drivers.sort(key=lambda x: (x.readable, x.writable))
        
    @property
    def defaultWrite(self) -> Driver:
        return self._drivers[0]
        
    def __contains__(self, key : str):
        for driver in self._drivers:
            if not driver.readable:
                continue
        
            if key in driver:
                return True
            
        return False
    
    def __getitem__(self, key : str):
        for driver in self._drivers:
            if not driver.readable:
                continue
        
            if key in driver:
                return driver[key]
            
        raise KeyError(key)
    
    def __setitem__(self, key : str, value):
        if self.defaultWrite.writable:
            self.defaultWrite[key] = value
            return
        
        for driver in self._drivers:
            if not driver.writable:
                continue
        
            driver[key] = value
            return
        
        raise RuntimeError("No writable drivers found.")
    
    def __delitem__(self, key : str):
        """
        this will delete the key from all writable drivers
        """
        for driver in self._drivers:
            if not driver.writable:
                continue
        
            del driver[key]
    
    @classmethod
    def createDefault(cls, path: str, configName: str):
        if not os.path.exists(os.path.join(path, f"{configName}.json")):
            dump_file({}, os.path.join(path, f"{configName}.json"))
        
        if not os.path.exists(os.path.join(path, f"{configName}.py")):
            with open(os.path.join(path, f"{configName}.py"), "w") as f:
                pass
        
        return cls([
            JsonDriver(os.path.join(path, f"{configName}.json")),
            PyDriver(os.path.join(path, f"{configName}.py")),
        ])