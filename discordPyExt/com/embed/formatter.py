from discord import Embed
from functools import cached_property

class embedFormatParser:
    def __init__(self, embed: Embed) -> None:
        self.embed = embed
        
    @cached_property
    def title_keywords(self):
        pass