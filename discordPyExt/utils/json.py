"""
this module aims to provide a faster json encoder and decoder
"""
_ORDER_OF_LOADING = [
    "orjson", "ujson", "json"
]

import importlib

_IMPORTED_JSON_MODULE = None
_IMPORTED_JSON_NAME = None
LOAD_FILE_METHOD = None
DUMP_FILE_METHOD = None
LOADS_METHOD = None
DUMPS_METHOD = None

def load_json_module(
    module_name=None,
    load_file_method=None,
    dump_file_method=None,
    loads_method=None,
    dumps_method=None
):
    global _IMPORTED_JSON_MODULE, _IMPORTED_JSON_NAME
    
    if module_name is not None:
        return _load_json_module(
            module_name=module_name,
            load_file_method=load_file_method,
            dump_file_method=dump_file_method,
            loads_method=loads_method,
            dumps_method=dumps_method
        )
    
    for module_name in _ORDER_OF_LOADING:
        try:
            return _load_json_module(
                module_name=module_name,
                load_file_method=globals().get(f"{module_name}_load_file", None),
                dump_file_method=globals().get(f"{module_name}_dump_file", None),
                loads_method=globals().get(f"{module_name}_loads", None),
                dumps_method=globals().get(f"{module_name}_dumps", None)
            )
        except ImportError:
            pass
        
def _load_json_module(
    module_name=None,
    load_file_method=None,
    dump_file_method=None,
    loads_method=None,
    dumps_method=None
):
    global _IMPORTED_JSON_MODULE, _IMPORTED_JSON_NAME, LOAD_FILE_METHOD, DUMP_FILE_METHOD, LOADS_METHOD, DUMPS_METHOD
    
    if module_name is None:
        raise ValueError("module_name cannot be None")
    
    if load_file_method is None:
        raise ValueError("load_file_method cannot be None")
    
    if dump_file_method is None:
        raise ValueError("dump_file_method cannot be None")
    
    if loads_method is None:
        raise ValueError("loads_method cannot be None")
    
    if dumps_method is None:
        raise ValueError("dumps_method cannot be None")
    
    _IMPORTED_JSON_MODULE = importlib.import_module(module_name)
    _IMPORTED_JSON_NAME = module_name
    LOAD_FILE_METHOD = load_file_method
    DUMP_FILE_METHOD = dump_file_method
    LOADS_METHOD = loads_method
    DUMPS_METHOD = dumps_method
    
    return _IMPORTED_JSON_MODULE

# orjson methods
def orjson_load_file(file_path):
    with open(file_path, "rb") as f:
        return _IMPORTED_JSON_MODULE.loads(f.read())

def orjson_dump_file(file_path, data):
    with open(file_path, "wb") as f:
        f.write(_IMPORTED_JSON_MODULE.dumps(data))
        
def orjson_loads(data):
    return _IMPORTED_JSON_MODULE.loads(data)

def orjson_dumps(data):
    return _IMPORTED_JSON_MODULE.dumps(data)

# ujson methods
def ujson_load_file(file_path):
    with open(file_path, "rb") as f:
        return _IMPORTED_JSON_MODULE.load(f)

def ujson_dump_file(file_path, data):
    with open(file_path, "wb") as f:
        _IMPORTED_JSON_MODULE.dump(data, f)
        
def ujson_loads(data):
    return _IMPORTED_JSON_MODULE.loads(data)

def ujson_dumps(data):
    return _IMPORTED_JSON_MODULE.dumps(data)

# json methods
def json_load_file(file_path):
    with open(file_path, "r") as f:
        return _IMPORTED_JSON_MODULE.load(f)
    
def json_dump_file(file_path, data):
    with open(file_path, "w") as f:
        _IMPORTED_JSON_MODULE.dump(data, f)
        
def json_loads(data):
    return _IMPORTED_JSON_MODULE.loads(data)

def json_dumps(data):
    return _IMPORTED_JSON_MODULE.dumps(data)

# auto load
load_json_module()

def load_file(file_path : str): return LOAD_FILE_METHOD(file_path)
def dump_file(file_path : str, data : dict): return DUMP_FILE_METHOD(file_path, data)
def loads(data : dict): return LOADS_METHOD(data)  
def dumps(data : dict): return DUMPS_METHOD(data)

__all__ = [
    "load_file",
    "dump_file",
    "loads",
    "dumps",
    "load_json_module",
]