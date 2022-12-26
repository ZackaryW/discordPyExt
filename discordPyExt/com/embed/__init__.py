
from discord import Embed
from discord.embeds import EmbedField
from pydantic import BaseModel
import typing
from functools import cached_property
from discordPyExt.com.embed.selector import xEmbedColorSelector, xEmbedStatusSelector

class xAuthor(BaseModel):
    name : str = None
    url : str = None
    icon_url : str = None

class xEmbedField(BaseModel):
    name : str
    value : str
    inline : bool = False

    def __call__(self):
        return EmbedField(**self.dict())

    @property
    def name_keyword(self):
        pass

class xFooter(BaseModel):
    text : str
    icon_url : str = None

    def __call__(self):
        return self.dict()
    
class xEmbed(BaseModel):
    title : str = None
    description : str = None
    url : str = None
    color : int = None
    timestamp : str = None
    footer : xFooter = None
    image : str = None
    thumbnail : str = None
    author : xAuthor = None
    fields : typing.List[xEmbedField] = None

    class Config:
        keep_untouched = (cached_property,)

    def __call__(self):
        self._embed = Embed(
            title=self.title,
            description=self.description,
            url=self.url,
            color=self.color,
            timestamp=self.timestamp,
        )
        if self.footer:
            self._embed.set_footer(**self.footer)
        if self.image:
            self._embed.set_image(self.image)
        if self.thumbnail:
            self._embed.set_thumbnail(self.thumbnail)
        if self.author:
            self._embed.set_author(**self.author.dict())
        if self.fields:
            for field in self.fields:
                self._embed.add_field(**field())
    
    @cached_property
    def colorSelector(self):
        return xEmbedColorSelector(self)
    
    @cached_property
    def statusSelector(self):
        return xEmbedStatusSelector(self)
    
    @classmethod
    def fromEmbed(cls, embed : Embed):
        author = xAuthor(**embed._author)
        footer = xFooter(**embed._footer)
        fields = [xEmbedField(**field) for field in embed._fields]
        color = embed._colour
        timestamp = embed._timestamp
        image = embed._image
        thumbnail = embed._thumbnail
        return cls(
            title=embed.title,
            description=embed.description,
            url=embed.url,
            color=color,
            timestamp=timestamp,
            footer=footer,
            image=image,
            thumbnail= thumbnail,
            author=author,
            fields=fields,
        )
