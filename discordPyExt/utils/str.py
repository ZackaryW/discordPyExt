
MATCH_TYPES = {
    "str" : str,
    "int" : int,
    "float" : float,
    "bool" : bool,
    "list" : list,
    "tuple" : tuple,
}

def get_format_vars(string : str):
    """
    parses a fstring and returns fields

    ex:
    "hello, {user}"

    returns ["user"]
    
    or 
    "hello, {user:str}"

    returns {"user" : str}
    
    """
    if string is None:
        return []
    
    if not isinstance(string, str):
        raise TypeError("string must be a string")
    
    # check if there are cases where the { is invalid
    if string.count("{") != string.count("}"):
        raise ValueError("invalid string")
    
    closed = True
    for char in string:
        if char == "{" and closed:
            closed = False
        elif char == "}" and not closed:
            closed = True
        elif char == "{" and not closed:
            raise ValueError("invalid string")
        elif char == "}" and closed:
            raise ValueError("invalid string")
    
    fields_dict = {}

    while string:
        if string[0] == "{":
            string = string[1:]
            field = ""
            while string:
                if string[0] == "}":
                    string = string[1:]
                    break
                field += string[0]
                string = string[1:]
            if ":" in field:
                field_name, field_type = field.split(":")
                fields_dict[field_name] = MATCH_TYPES[field_type]
            else:
                fields_dict[field] = None
        else:
            string = string[1:]
            
    # if all values are none, return list(keys)
    if all([x is None for x in fields_dict.values()]):
        return list(fields_dict.keys())
            
    return fields_dict

def format_string(string : str, format_vars =None, **kwargs):
    
    if format_vars is None:
        vars = get_format_vars(string)
    else:
        vars = format_vars
    # filter kwargs
    kwargs = {k:v for k,v in kwargs.items() if k in vars}
    
    if isinstance(vars, dict):
        # check kwargs types
        for k,v in kwargs.items():
            if not isinstance(v, vars[k]):
                raise TypeError(f"{k} must be a {vars[k]}")
    
    return string.format(**kwargs)
    