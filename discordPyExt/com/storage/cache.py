
import asyncio
import typing
from discordPyExt.com.storage.driver import Driver
import discord
from discord.ext import commands
from pydantic import BaseModel, validator
import inspect

async def get_or_fetch(get_method, fetch_method, id):
    obj = get_method(id)
    if obj is None:
        obj = await fetch_method(id)
    return obj

class DCC(BaseModel):
    """
    discord cache container
    """
    id : int
    type : typing.Literal["user", "role", "channel", "guild"]
    dependsOn : typing.Optional[str] 
    
    @validator("id")
    def id_must_be_int(cls, v):
        return int(v)
    
    async def fetch(self, bot : commands.Bot, depender : discord.Object = None):
        if self.type == "user":
            return await get_or_fetch(bot.get_user, bot.fetch_user, self.id)
        elif self.type == "role" and depender is not None and isinstance(depender, discord.Guild):
            return await get_or_fetch(depender.get_role, None, self.id)
        elif self.type == "channel" and depender is not None and isinstance(depender, discord.Guild):
            return await get_or_fetch(depender.get_channel, depender.fetch_channel, self.id)
        elif self.type == "guild":
            return await get_or_fetch(bot.get_guild, bot.fetch_guild, self.id)
        else:
            raise ValueError(f"Invalid type: {self.type}")
    
class Cache:
    def __init__(self, bot : commands.Bot, driver : Driver |dict) -> None:
        self._rawdata = driver
        self._objdata = {}
        self._bot = bot
        
    def __contains__(self, key : str):
        return key in self._jsondata    
    
    async def __getitem__(self, key : str):
        if key in self._objdata:
            return self._objdata[key]

        raw = self._rawdata.get(key, None)
        if raw is None:
            raise KeyError(key)
        
        if isinstance(raw, dict):
            raw = DCC(**raw)
            dependsOn = self._objdata.get(raw.dependsOn, None)
            self._objdata[key] = await raw.fetch(self._bot, dependsOn)
        elif isinstance(raw, DCC):
            dependsOn = self._objdata.get(raw.dependsOn, None)
            self._objdata[key] = await raw.fetch(self._bot, dependsOn)
        elif isinstance(raw, int) or isinstance(raw, str):
            self._objdata[key] = discord.Object(int(raw))
        return self._objdata[key]
    
    async def get(self, key : str, default = None):
        try:
            return await self[key]
        except KeyError:
            return default
    
    def set(self, key : str, value:  typing.Union[int, str, discord.Object]):
        self._objdata[key] = value
    
    def keys(self):
        return self._rawdata.keys()
    
    async def values(self):
        for key in self.keys():
            yield await self[key]
            
    async def items(self):
        for key in self.keys():
            yield key, await self[key]
            
    async def preloadAll(self, interval : int = 0):
        for key in self.keys():
            if interval > 0:
                await asyncio.sleep(interval)
            await self[key]