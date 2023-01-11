from discord.ext import commands
from discord import app_commands
import discord
from discordPyExt.com.storage.cache import Cache

from discordPyExt.com.storage.driver import Driver
class xBot(commands.Bot):
    """
    a bot with default setup behavior and builtin preloading/caching of discord objects
    """
    def __init__(
        self, 
        *,
        tree_cls = app_commands.CommandTree, 
        description = None, 
        intents: discord.Intents =discord.Intents.default(), 
        command_prefix= "!", 
        **options,
    ) -> None:
        super().__init__(
            command_prefix, 
            tree_cls=tree_cls,
            description=description,
            intents=intents,
            **options)
        self._cache = None
        self._cache_load_all = False
        self._cache_load_interval = 1
        
    def addCache(self, driver: Driver, loadAll : bool = False):
        self._cache = Cache(self, driver)
        self._cache_load_all = loadAll
    
    async def on_ready(self):
        print("Logged in as {0.user}".format(self))
        if self._cache is not None and self._cache_load_all:
            await self._cache.preloadAll(self._cache_load_interval)

    async def setup_hook(self) -> None:
        await self.tree.sync()
    
    @property
    def cache(self) -> Cache:
        return self._cache
    
    