import os
import typing
import orjson

class DataDriver:
    """
    a DataDriver represents a storage container / interface
    
    * path is initilized as a child of DataLoader
    """
    
    _settable : bool = None     
    """
    if __setattr__can be used
    """
        
    _default_path : str = None
    """
    default file path
    """

    def __init__(self, path: str =None) -> None:
        return
        
    def __contains__(self, key):
        raise NotImplementedError
    
    def __getitem__(self, key):
        raise NotImplementedError
    
    def __setitem__(self, key, value):
        raise NotImplementedError

    def _supported(self, val):
        """
        Check if the value is supported by the driver
        
        ex: json only supports dict, list, str, int, float, bool, None
        """
        return True
    
    def get(self, name : str, default = None):
        """
        get a value from the config
        
        if the value is not found, return default
        """
        if not self.__contains__(name):
            return default
        
        return self.__getitem__(name)

    def items(self):
        """
        yield all items
        """
        raise NotImplementedError

class DataLoader:    
    """
    Dataloader is just like a dict, but with multiple drivers
    
    for example: 
    suppose you have a json file, a python file and a database (driver not implemented)

    you can set a priority order for the drivers, and the dataloader will get the value from the first driver that has the value

    """
    
    def _add_non_driver(self, driver):
        """
        in many cases, a driver as an wrapper for a non-driver with existing `__getitem__`,
        `__setitem__` and `__contains__` methods 
        is redundant, so this method is used to add a non-driver to the dataloader
        """
        
        if not hasattr(driver, "__getitem__"):
            raise TypeError(f"missing __getitem__")
        if not hasattr(driver, "__contains__"):
            raise TypeError(f"missing __contains__")
        if hasattr(driver, "__setitem__"):
            self._settables.append(driver)
        self._drivers.append(driver)
    
    def __init__(
        self, 
        path: str, 
        *drivers, 
        allow_non_driver: bool = False, 
        default_settable = None,
        set_only_default : bool = False,
    ) -> None:
        
        self._set_only_default = set_only_default
        
        # check if contain duplicates
        if len(drivers) != len(set(drivers)):
            raise ValueError("duplicate drivers")
        
        self._drivers : typing.List[DataDriver] = []
        """
        a list of drivers
        """
        
        self._settables : typing.List[DataDriver] = []
        """
        a list of drivers that has __setitem__
        """
        
        # loop through drivers
        for i, driver in enumerate(drivers):
            driver: DataDriver
            not_config_driver =not (isinstance(driver, DataDriver)or issubclass(driver, DataDriver))
            
            # if it is a non-driver
            if allow_non_driver and not_config_driver:
                self._add_non_driver(driver)
                continue
            
            # not a driver and not allowed
            if not_config_driver:
                raise TypeError(f"Argument {i} must be of type DataDriver")
        
            if isinstance(driver, type):
                if driver._default_path is None:
                    driver = driver(path=path)
                else:
                    driver = driver(path=os.path.join(path, driver._default_path))
    
            if driver._settable:
                self._settables.append(driver)
            
            self._drivers.append(driver) 
            
        # sets default
        self._default_settable = default_settable
        if self._default_settable is None and len(self._settables) > 0:
            # get first in list
            self._default_settable = self._settables[0]
        
    def __getattribute__(self, __name: str):
        if __name.startswith("_") or __name in ["get", "noDupSet", "getDriver"]:
            return super().__getattribute__(__name)
        
        # loop through drivers
        for driver in self._drivers:
            if __name in driver:
                return driver[__name]
            
        raise AttributeError(f"attribute {__name} not found")

    def __setattr__(self, __name: str, __value: typing.Any):
        if __name.startswith("_"):
            return super().__setattr__(__name, __value)
        
        # check if settables is empty
        if len(self._settables) == 0:
            raise AttributeError(f"no settables found")
        
        # check default settable and whether the value is supported
        if (
            self._default_settable is not None 
            and self._default_settable._supported(__value)
        ):
            self._default_settable[__name] = __value
            return
        
        # if set only default, raise error
        if self._set_only_default :
            raise AttributeError(f"attribute {__name} not settable")
        
        for driver in self._settables:
            if driver == self._default_settable:
                continue
            
            if not driver._supported(__value):
                continue
                
            try:
                driver[__name] = __value
                return
            except:
                continue
        
        raise AttributeError(f"attribute {__name} not found")
        
    def getDriver(self, name : str) -> typing.Optional[DataDriver]:
        """
        gets the first driver that has the attribute
        """
        
        for driver in self._drivers:
            if name in driver:
                return driver
        return None
        
    def get(self, name : str, default = None):
        """
        get a value from the config with default return
        """
        return getattr(self, name, default)
    

    def noDupSet(self, key, val):
        """
        this method ensures when setting a value, it will not be set to multiple drivers
        """
        
        driver = self.getDriver(key)
        if driver is None:
            setattr(self, key, val)
        elif driver not in self._settables:
            raise AttributeError(f"attribute {key} not settable")
        else:
            driver[key] = val        
    
    @classmethod
    def create_default(cls, path : str) -> "DataLoader":
        """
        creates a dataloader with a PyFileDriver and a JsonDriver
        """
        
        os.makedirs(path, exist_ok=True)
        if not (os.path.exists(os.path.join(path, "config.json"))):
            with open(os.path.join(path, "config.json"), "w") as f:
                f.write("{}")
        if not (os.path.exists(os.path.join(path, "config.py"))):
            with open(os.path.join(path, "config.py"), "w") as f:
                f.write("")
        
        return cls(path, PyFileDataDriver, JsonDataDriver,             
            allow_non_driver=True,
            default_settable=None
        )
    
class JsonDataDriver(DataDriver):
    _default_path: str = "config.json"
    _settable : bool = True
    
    def __init__(self, path : str = None) -> None:
        if path is None:
            path = self._default_path    
    
        if not os.path.exists(path):
            raise FileNotFoundError(f"file {path} not found")
        
        self._path : str = path
        self._data : dict = {}
        with open(path, "rb") as f:
            self._data = orjson.loads(f.read())
        
        
        super().__init__()
        self._settable = True
        
    def __contains__(self, key):
        return key in self._data
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __setitem__(self, key, value):
        self._data[key] = value
        with open(self._path, "wb") as f:
            f.write(orjson.dumps(self._data))
            
    def _supported(self, val):
        # check if json serializable
        try:
            orjson.dumps(val)
            return True
        except:
            return False
    
    def items(self):
        return self._data.items()
    
        
class PyFileDataDriver(DataDriver):
    _default_path: str = "config.py"
    _settable : bool = False
    
    def __init__(self, path : str = None) -> None:
        if path is None:
            path = self._default_path    
    
        if not os.path.exists(path):
            raise FileNotFoundError(f"file {path} not found")
        
        self._path : str = path
        self._data : dict = {}
        with open(path, "rb") as f:
            exec(f.read(), self._data)
            
        # filter data _
        self._data = {key: value for key, value in self._data.items() if not key.startswith("_")}
        
    
        super().__init__()
        self._settable = False
        
    def __contains__(self, key):
        return key in self._data

    def __getitem__(self, key):
        return self._data[key]
        
    def items(self):
        return self._data.items()