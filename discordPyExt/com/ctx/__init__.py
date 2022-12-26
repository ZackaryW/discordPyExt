import discord
from discord.ext import commands
import typing
from pydantic import BaseModel
from enum import Enum
import inspect
import discordPyExt.com.ctx.funcs as _ctx

class xCtx:
    @classmethod
    def match( 
        cls,
        *args : typing.List['xCtxType'],
        **kwargs,     
    ):
        """
        since all the functions are decorated with addFuncArgs, 
        the args needed are stored in the function's __funcargs
        """
        
        res = []
        for arg in args:
            arg : xCtxType
            val = arg.type.value(*arg.args, **{k : v for k, v in kwargs.items() if k in arg.type.value.__funcargs})
            res.append(val)
        
        return res
    
    def __init__(self,
        args : typing.Union[typing.List['xCtxType'], typing.Dict[str, 'xCtxType']],
        **kwargs,     
    ) -> None:
        self.matchKeys = None
        if isinstance(args, dict):
            self.matchKeys = list(args.keys())
        self.res = self.match(*args, **kwargs)

    def __getitem__(self, key : typing.Union[int, str]):
        if isinstance(key, int):
            return self.res[key]
        elif isinstance(key, str) and self.matchKeys is not None:
            return self.res[self.matchKeys.index(key)]
        elif isinstance(key, str) and self.matchKeys is None:
            # never init error
            raise KeyError(f"str key never init")
        else:
            raise KeyError(f"key {key} not found")
        

class xCtxEnum:
    ctx_has_role = _ctx.ctx_has_role
    ctx_has_any_role = _ctx.ctx_has_any_role
    user_has_any_role = _ctx.user_has_any_role
    user_has_role = _ctx.user_has_role
    ctx_get_role = int
    ctx_get_any_role = int
    ctx_get_user = int
    ctx_get_any_user = int
    user_get_any_role = int
    user_get_role = int 
    ctx_has_permission = _ctx.ctx_has_permission
    ctx_has_any_permission = _ctx.ctx_has_any_permission
    user_has_any_permission = _ctx.user_has_any_permission
    user_has_permission = _ctx.user_has_permission

class xCtxType:
    type : typing.Callable
    args : typing.List[typing.Any]

    def __init__(self, type, args) -> None:
        self.type = type
        self.args = args

ctx_has_role = lambda *args : xCtxType(type=xCtxEnum.ctx_has_role, args=args)
ctx_has_any_role = lambda *args : xCtxType(type=xCtxEnum.ctx_has_any_role, args=args)
user_has_any_role = lambda *args : xCtxType(type=xCtxEnum.user_has_any_role, args=args)
user_has_role = lambda *args : xCtxType(type=xCtxEnum.user_has_role, args=args)
ctx_get_role = lambda *args : xCtxType(type=xCtxEnum.ctx_get_role, args=args)
ctx_get_any_role = lambda *args : xCtxType(type=xCtxEnum.ctx_get_any_role, args=args)
ctx_get_user = lambda *args : xCtxType(type=xCtxEnum.ctx_get_user, args=args)
ctx_get_any_user = lambda *args : xCtxType(type=xCtxEnum.ctx_get_any_user, args=args)
user_get_any_role = lambda *args : xCtxType(type=xCtxEnum.user_get_any_role, args=args)
user_get_role = lambda *args : xCtxType(type=xCtxEnum.user_get_role, args=args)
ctx_has_permission = lambda *args : xCtxType(type=xCtxEnum.ctx_has_permission, args=args)
ctx_has_any_permission = lambda *args : xCtxType(type=xCtxEnum.ctx_has_any_permission, args=args)
user_has_any_permission = lambda *args : xCtxType(type=xCtxEnum.user_has_any_permission, args=args)
user_has_permission = lambda *args : xCtxType(type=xCtxEnum.user_has_permission, args=args)
