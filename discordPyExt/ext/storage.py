import typing

class Storage(dict):
    def __getattribute__(self, __name: str):
        if __name in self:
            return self[__name]
        else:
            return super().__getattribute__(__name)
        
    def __setattr__(self, __name: str, __value: typing.Any):
        if __name.startswith("_"):
            super().__setattr__(__name, __value)
        else:
            self[__name] = __value