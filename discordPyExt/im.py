"""
provides easy import at the cost of performance
"""

from discord.ext import commands
import discord
from discord import (
    Interaction, Embed, Guild, TextChannel, ForumChannel, GroupChannel, ForumTag, 
    Role, Member, User, Emoji, PartialEmoji, Message, MessageReference, File, 
    Asset, Invite, StageInstance, 
    StageChannel, Thread, ThreadMember,
    VoiceChannel, CategoryChannel, DMChannel, Colour, Color, 
    Permissions, PermissionOverwrite, Activity, ActivityType, Intents
)
from discord.ui import (
    View, Button, Select, Modal
)
