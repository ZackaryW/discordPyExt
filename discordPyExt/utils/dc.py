
import logging
import os
import typing
from discord.ext import commands

from discordPyExt.utils.doNothing import DO_NOTHING_OBJECT

async def load_extensions(
    bot : commands.Bot,
    folder_path : str,
    skip_extensions : typing.List[str],
    logger : logging.Logger = DO_NOTHING_OBJECT
):
    if not os.path.isdir(folder_path):
        raise ValueError(f'Folder {folder_path} does not exist!')
    
    for file_name in os.listdir(folder_path):
        if not file_name.endswith('.py') or file_name.startswith('_'):
            continue
        
        extension_name = file_name[:-3]
        if extension_name in skip_extensions:
            continue
        
        try:
            await bot.load_extension(f'{folder_path}.{extension_name}')
        except Exception as e:
            logger.error(f'Failed to load extension {extension_name}!', exc_info=e)
        else:
            logger.info(f'Loaded extension {extension_name}!')
            
            
