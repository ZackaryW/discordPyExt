import unittest
from discordPyExt.com.ctx import *
from discord.ext import commands
from discord import Interaction

class t_com_ctx(unittest.TestCase):
    def test_1(self):
        ctx : Interaction = None
        bot : commands.Bot = None

        args=(
            ctx_has_role("test"),
            ctx_has_any_role("test"),
            user_has_any_role("test"),
            user_has_role("test"),
            ctx_get_role("test"),
            ctx_get_any_role("test"),
            ctx_get_user("test"),
            ctx_get_any_user("test"),
            user_get_any_role("test"),
            user_get_role("test"),
            ctx_has_permission("test"),
            ctx_has_any_permission("test"),
            user_has_any_permission("test"),
            user_has_permission("test"),
        )
        
        _has_role, _has_any_role, *args = xCtx.match(
            ctx=ctx,
            bot=bot,
            
        )
