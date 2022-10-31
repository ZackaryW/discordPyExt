import os
import typing
import inspect
import importlib


def import_objs(
    folder_path : str, 
    target : typing.Union[str, type] = None, 
    ignore_slash : bool = True, 
    only_object: bool = True, 
    only_type: bool = False,
    skip_names : typing.List[str] = [],
):
    # list all files
    python_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(".py")]
    
    # folder path to package format
    folder_package = folder_path.replace("\\", ".").replace("/", ".")
    
    # import all files
    for file in python_files:
        pkg = importlib.import_module(f"{folder_package}.{os.path.splitext(file)[0]}")

        if target is None:
            yield pkg
            continue
        
        for name, obj in inspect.getmembers(pkg):
            if ignore_slash and name.startswith("_"):
                continue
            
            if name in skip_names:
                continue
        
            if isinstance(target, str) and name == target:
                yield obj
                break
            elif only_object and isinstance(obj, target) and obj != target:
                yield obj
                break
            
            elif only_type and isinstance(obj, type) and issubclass(obj, target) and obj != target:
                yield obj
                break
        
