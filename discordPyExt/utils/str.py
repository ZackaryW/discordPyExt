import typing

def formatVars(
    string : str, 
):
    """
    parses a fstring and return a list of fields
    """
    # check count
    if string.count("{") != string.count("}"):
        raise TypeError("invalid fstring")
    
    fields = []
    
    while True:
        # find first {
        start = string.find("{")
        if start == -1:
            break
        # find first }
        end = string.find("}")
        if end == -1:
            raise TypeError("invalid fstring")
        # get field
        field = string[start+1:end]
        fields.append(field)
        
        # remove from string
        string = string[end+1:]
    
    return fields
        
        
def parseVars(fstring :str, cstring :str, fields :list,knowings : dict):
    
    
    if fields is None:
        return knowings
        
    nstring = fstring
    
        
    for field in fields:
        if field in knowings:
            nstring = nstring.replace("{" + field + "}", knowings[field])
    
    missing_fields = [f for f in fields if f not in knowings]
    
    if len(missing_fields) == 0:
        return knowings
    
    import parse

    try:
        res = parse.parse(nstring, cstring).named
        knowings.update(res)
        
    except:
        pass
    
    return knowings