class DoNothing:
    """
    this class does absolutely nothing
    
    example:
    
    obj.something1(x=1, y=2).something2().something3()()
    
    """
    
    def __getattribute__(self, __name: str):
        if __name.startswith('__'):
            return object.__getattribute__(self, __name)
        
        return self
    
    def __call__(self, *args, **kwds):
        return self
    
DO_NOTHING_OBJECT = DoNothing() 
