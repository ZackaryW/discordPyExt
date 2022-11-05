from discord.ext import commands
import typing
from discord import app_commands    

class ExtendedCog:
    bot : commands.Bot
    
    def __init__(self) -> None:
        self._manual_registers = {}
    
    async def cog_unload_manual(self) -> None:
        for name, item in self._manual_registers.items():
            self.bot.tree.remove_command(name, item.type)

    def add_context_menu(self, name : str, func: typing.Callable):
        ctx_menu_item = app_commands.ContextMenu(
            name=name,
            callback=func,
        )
        self._manual_registers[name] = ctx_menu_item
        

    def sync_manual(self):
        for name, item in self._manual_registers.items():
            self.bot.tree.add_command(item)

class CogX(ExtendedCog, commands.Cog):
    def __init__(self) -> None:
        self._manual_registers = {}
        super().__init__()
    
    async def cog_load(self) -> None:
        self.sync_manual()
        await super().cog_load()
    
    async def cog_unload(self) -> None:
        self.cog_unload_manual()
        await super().cog_unload()
        
class GroupCogX(ExtendedCog, commands.GroupCog):
    def __init__(self) -> None:
        self._manual_registers = {}
        super().__init__()
    
    async def cog_load(self) -> None:
        self.sync_manual()
        await super().cog_load()
    
    async def cog_unload(self) -> None:
        await self.cog_unload_manual()
        await super().cog_unload()