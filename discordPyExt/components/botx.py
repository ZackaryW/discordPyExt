from discord.ext import commands
from discord import Intents
import discord

class BotX(commands.Bot):
    """
    an extension of the discord.py bot class
    """
    
    def __init__(
        self, command_prefix = "!", 
        intents : Intents = Intents.all()
    ) -> None:
        super().__init__(command_prefix=command_prefix, intents=intents)
        
    def get_or_fetch(self, obj_type : discord.Object, id : int):
        """
        ## allowed types
        - discord.User
        - discord.Guild
        - discord.abc.GuildChannel (discord.TextChannel/ discord.VoiceChannel/ discord.CategoryChannel/ discord.StageChannel)
        
        """
        
        if obj_type == discord.User:
            return self.get_user(id) or self.fetch_user(id)
        elif (
            issubclass(obj_type, discord.abc.GuildChannel)
        ):
            return self.get_channel(id) or self.fetch_channel(id)
        elif obj_type == discord.Guild:
            return self.get_guild(id) or self.fetch_guild(id)
        else:
            raise ValueError(f'Unknown object type {obj_type}!')
        
    def guild_get_or_fetch(self, obj_type : discord.Object, guild : discord.Guild , id : int):
        """
        ## allowed types
        - discord.Role
        - discord.Member
        """
        
        if obj_type == discord.Role:
            return guild.get_role(id)
        elif obj_type == discord.Member:
            return guild.get_member(id) or guild.fetch_member(id)
        else:
            raise ValueError(f'Unknown object type {obj_type}!')
        
    async def on_ready(self):
        print("Logged in as {0.user}".format(self))
        
    async def setup_hook(self) -> None:
        await self.tree.sync()