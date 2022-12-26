import discord
from discord.ext import commands
import typing
from discordPyExt.utils.funcArgs import addFuncArgs

@addFuncArgs(
    args= ("ctx", "bot"),
)
def ctx_has_role(ctx : discord.Interaction, bot : commands.Bot = None, *query_roles : typing.Union[discord.Role, int, str]) -> bool:
    """
    check if the user has any role in guild
    """
    uids = [role.id for role in ctx.user.roles]
    
    for role in ctx.user.roles:
        if isinstance(role, discord.Role) and role not in query_roles:
            return False
        if isinstance(role, int) and role not in uids:
            return False
        if isinstance(role, str) and int(role) not in uids:
            return False
    
    return True

@addFuncArgs(
    args= ("ctx", "bot"),
)
def ctx_has_any_role(ctx : discord.Interaction, bot : commands.Bot = None, *query_roles : typing.Union[discord.Role, int, str]) -> bool:
    """
    check if the user has any role in guild
    """
    uids = [role.id for role in ctx.user.roles]
    
    for role in ctx.user.roles:
        if isinstance(role, discord.Role) and role in query_roles:
            return True
        if isinstance(role, int) and role in uids:
            return True
        if isinstance(role, str) and int(role) in uids:
            return True
    
    return False

@addFuncArgs(
    args= ("user"),
)
def user_has_any_role(
    user : discord.User, 
    *query_roles : typing.Union[discord.Role, int, str]
) -> bool:
    """
    check if the user has any role in guild
    """
    if not isinstance(user, discord.User):
        raise TypeError("user must be discord.User")
    
    uids = [role.id for role in user.roles]
    
    for role in user.roles:
        if isinstance(role, discord.Role) and role in query_roles:
            return True
        if isinstance(role, int) and role in uids:
            return True
        if isinstance(role, str) and int(role) in uids:
            return True
    
    return False

@addFuncArgs(
    args= ("user"),
)
def user_has_role(
    user : discord.User, 
    *query_roles : typing.Union[discord.Role, int, str]
) -> bool:
    """
    check if the user has any role in guild
    """
    if not isinstance(user, discord.User):
        raise TypeError("user must be discord.User")
    
    uids = [role.id for role in user.roles]
    
    for role in user.roles:
        if isinstance(role, discord.Role) and role not in query_roles:
            return False
        if isinstance(role, int) and role not in uids:
            return False
        if isinstance(role, str) and int(role) not in uids:
            return False
    
    return True

@addFuncArgs(
    args= ("ctx", "bot"),
)
def ctx_has_permission(ctx : discord.Interaction, bot : commands.Bot = None, **kwargs) -> bool:
    """
    check if the user has permission in guild
    """
    return all(getattr(ctx.user.guild_permissions, name, None) == value for name, value in kwargs.items())

@addFuncArgs(
    args= ("ctx", "bot"),
)
def ctx_has_any_permission(ctx : discord.Interaction, bot : commands.Bot = None, **kwargs) -> bool:
    """
    check if the user has any permission in guild
    """
    return any(getattr(ctx.user.guild_permissions, name, None) == value for name, value in kwargs.items())

@addFuncArgs(
    args= ("user"),
)
def user_has_any_permission(
    user : discord.Member, 
    **kwargs
) -> bool:
    """
    check if the user has any permission in guild
    """
    if not isinstance(user, discord.User):
        raise TypeError("user must be discord.User")
    
    return any(getattr(user.guild_permissions, name, None) == value for name, value in kwargs.items())

@addFuncArgs(
    args= ("user"),
)
def user_has_permission(
    user : discord.Member,
    **kwargs
) -> bool:
    """
    check if the user has permission in guild
    """
    if not isinstance(user, discord.User):
        raise TypeError("user must be discord.User")
    
    return all(getattr(user.guild_permissions, name, None) == value for name, value in kwargs.items())