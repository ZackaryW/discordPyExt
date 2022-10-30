
import os
import discord
from discordPyExt.setup.extension import DcExtension
from discordPyExt.components.botx import BotX
from discordPyExt.utils.dc import load_extensions

class DeployBot(DcExtension):
    """
    ! you don't need to add this extension to DcDeployer, it is builtin
    """
    
    _hash = "BOT"
    
    async def init(
        self,
        DISCORD_TOKEN : str,
        DISCORD_OBJ : discord.Client = BotX,
        DISCORD_COMMAND_PREFIX : str = "!",
        DISCORD_COG_FOLDER : str = "dcogs",
        DISCORD_COG_SUBFOLDER_OF_PROJECT : bool = True,
        DISCORD_DISABLE_EXTENSIONS : list = [],
       
    ) -> None:
        self.discord_obj : BotX = DISCORD_OBJ(
            command_prefix=DISCORD_COMMAND_PREFIX
        )

        if DISCORD_COG_SUBFOLDER_OF_PROJECT:
            DISCORD_COG_FOLDER = f"{self._base.path}/{DISCORD_COG_FOLDER}"
        
        await load_extensions(self.discord_obj, DISCORD_COG_FOLDER, DISCORD_DISABLE_EXTENSIONS, self._base.logger.getChild("Bot"))
        
        self.discord_token = DISCORD_TOKEN
        
    def setup(
        self,
        DISCORD_COG_FOLDER : str = "dcogs",
        DISCORD_COG_SUBFOLDER_OF_PROJECT : bool = True,
    ) -> None:
        if DISCORD_COG_SUBFOLDER_OF_PROJECT:
            DISCORD_COG_FOLDER = f"{self._base.path}/{DISCORD_COG_FOLDER}"
        
        os.makedirs(DISCORD_COG_FOLDER, exist_ok=True)
    
    def run(self):
        self.discord_obj.run(self.discord_token)
        