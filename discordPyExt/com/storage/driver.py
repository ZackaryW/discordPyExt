import os


class Driver:
    def __init__(self, path : str) -> None:
        self._data : dict = None
        self._path : str = path
        self.load(path)
        
    @property
    def readable(self) -> bool:
        return True
    
    @property
    def writable(self) -> bool:
        return False
    
    def load(self, data : str | dict):
        if isinstance(data, dict):
            self._data = data
        raise TypeError("Data must be a dict")
        
    def save(self):
        if not self.writable:
            raise RuntimeError("This driver is not writable.")
        raise NotImplementedError("This driver does not implement save.")
    
    def get(self, key : str, default = None):
        if not self.readable:
            raise RuntimeError("This driver is not readable.")
        
        return self._data.get(key, default)
    
    def set(self, key : str, value):
        if not self.writable:
            raise RuntimeError("This driver is not writable.")
        
        if value is None and key in self._data:
            del self._data[key]
        else:
            self._data[key] = value
        self.save()

    def __contains__(self, key : str):
        return key in self._data

    def __getitem__(self, key : str):
        return self._data[key]
    
    def __setitem__(self, key : str, value):
        return self.set(key, value)
    
    def __delitem__(self, key : str):
        return self.set(key, None)
    
    def items(self):
        return self._data.items()
    
    def keys(self):
        return self._data.keys()
    
    def values(self):
        return self._data.values()
    
    def __iter__(self):
        return iter(self._data)
    
    def __len__(self):
        return len(self._data)
    
    def __repr__(self):
        return f"<{self.__class__.__name__} path={self._path}>"
    
    def __str__(self):
        return repr(self)
    
    def __eq__(self, other):
        return self._data == other._data
    
from discordPyExt.utils.json import load_file, dump_file

class JsonDriver(Driver):
    @property
    def readable(self) -> bool:
        return True
    @property
    def writable(self) -> bool:
        return True
    
    def load(self, path : str):
        super().load(load_file(path))
    
    def save(self):
        dump_file(self._data, self._path)

    def set(self, key : str, value = None):
        if value is None and key in self._data:
            del self._data[key]
        else:
            self._data[key] = value
        self.save(self._path)

import toml

class TomlDriver(Driver):
    @property
    def readable(self) -> bool:
        return True
    @property
    def writable(self) -> bool:
        return True
    
    def load(self, path : str):
        super().load(toml.load(path))
        
    def save(self, path : str):
        with open(path, "w") as f:
            toml.dump(self._data, f)
    
class PyDriver(Driver):
    @property
    def readable(self) -> bool:
        return True
    @property
    def writable(self) -> bool:
        return False
    
    def load(self, path : str):
        with open(path, "r") as f:
            exec(f.read(), self._data)
    
class MemoryDriver(Driver):
    def __init__(self) -> None:
        self._data : dict = {}
        self._path : str = None
    
    @property
    def readable(self) -> bool:
        return True
    @property
    def writable(self) -> bool:
        return True
    
  
    
    def save(self):
        pass