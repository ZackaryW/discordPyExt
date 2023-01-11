from functools import cached_property
from uuid import uuid4
from pydantic import BaseModel, Field
import typing
from discordPyExt.utils.str import formatVars, parseVars
import discord
from discord import Embed
from functools import cached_property
from discordPyExt.com.embed.selector import xEmbedColorSelector, xEmbedStatusSelector

class BaseModelWithCachedProperty(BaseModel):
    class Config:
        keep_untouched = (cached_property,)
    
class FormatVarsSupport:
    @cached_property
    def vars(self : BaseModel):
        vals = {}
        for k, v in self.__fields__.items():
            if v.type_ != str:
                continue
            
            rv = getattr(self, k, None)
            
            if rv is None:
                continue
            
            if not("{" in rv and "}" in rv):
                continue    
                
            vals[k] = formatVars(rv)

        return vals 
    
    def _format(
        self, 
        fstring : str, 
        var_key : str,
        extras : typing.Dict[str, 'xEmbedFormatField'], 
        **kwargs
    ):
        if fstring is None:
            return None
        
        if var_key is None:
            return fstring
        
        vars = self.vars.get(var_key, None)
        
        if vars is None:
            raise ValueError(f"no vars for {var_key}")
        
        inputArgs = {}
        for var in vars:
            var_in_kwargs = var in kwargs
            var_in_extras = var in extras
            
            if not var_in_extras and not var_in_kwargs:
                raise ValueError(f"no value for {var}")
            elif var_in_extras and not var_in_kwargs:
                inputArgs[var] = extras[var].input(_DEFAULT_FLAG)
            elif not var_in_extras and var_in_kwargs:
                inputArgs[var] = kwargs[var]
            elif var_in_extras and var_in_kwargs:
                inputArgs[var] = extras[var].input(kwargs[var])
                
        return fstring.format_map(inputArgs)
        

class xAuthor(BaseModelWithCachedProperty, FormatVarsSupport):
    """
    embed author
    """
    name : str = None
    url : str = None
    icon_url : str = None

class xEmbedField(BaseModelWithCachedProperty, FormatVarsSupport):
    """
    embed field
    """
    name : str
    value : str
    inline : bool = False

class xFooter(BaseModelWithCachedProperty, FormatVarsSupport):
    """
    embed footer
    """
    text : str
    icon_url : str = None

_DEFAULT_FLAG = object()

class xEmbedFormatField(BaseModelWithCachedProperty, FormatVarsSupport):
    class Config:
        arbitrary_types_allowed = True

    input_type : type = None
    parse_lambda : typing.Callable = None
    parse_type : type = None
    export_lambda : typing.Callable = None
    export_type : type = None       
    default : typing.Any = None
    default_factory : typing.Callable = None
    
    def input(self, v):
        if v == _DEFAULT_FLAG and self.default is not None:
            v = self.default
        elif v == _DEFAULT_FLAG and self.default_factory is not None:
            v = self.default_factory()
        else:
            raise ValueError("no default value set")

        if self.input_type is not None and not isinstance(v, self.input_type):
            raise TypeError(f"expected type {self.input_type}, got {type(v)}")

        if self.parse_lambda is not None:
            v = self.parse_lambda(v)
        
        if self.parse_type is not None:
            v = self.parse_type(v)
        
        return v
            

class xEmbed(BaseModel, FormatVarsSupport):
    """
    this is a pydantic model of an embed
    """
    class Config:
        arbitrary_types_allowed = True
        keep_untouched = (cached_property,)
    
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
    extras : typing.Dict[str, xEmbedFormatField] = Field(default_factory=dict)
    cache : typing.Any = None
    
    def setFormatDefaults(self, **kwargs):
        def _set(f : xEmbedFormatField, v):
            if isinstance(v, type):
                f.input_type = v
            elif isinstance(v, typing.Callable):
                f.default_factory = v
            else:
                f.default = v
        
        for k, v in kwargs.items():
            if k not in self.extras:
                self.extras[k] = xEmbedFormatField()

            if isinstance(v, typing.Iterable):
                for vv in v:
                    _set(self.extras[k], vv)
            else:
                _set(self.extras[k], v)
                        
    
    @cached_property
    def colorSelector(self):
        return xEmbedColorSelector(self)
    
    @cached_property
    def statusSelector(self):
        return xEmbedStatusSelector(self)
    
    @classmethod
    def fromEmbed(cls, embed : discord.Embed):
         return cls(
            title=embed.title,
            description=embed.description,
            url=embed.url,
            color=embed.color.value if embed.color else None,
            timestamp=embed.timestamp,
            footer=xFooter(text=embed.footer.text, icon_url=embed.footer.icon_url) if embed.footer else None,
            image=embed.image.url if embed.image else None,
            thumbnail=embed.thumbnail.url if embed.thumbnail else None,
            author=xAuthor(name=embed.author.name, url=embed.author.url, icon_url=embed.author.icon_url) if embed.author else None,
            fields=[xEmbedField(name=field.name, value=field.value, inline=field.inline) for field in embed.fields] if embed.fields else None,
        )
         
    def toEmbed(self, **kwargs):
        title = kwargs.get("title", self.title)
        description = kwargs.get("description", self.description)
        url = kwargs.get("url", self.url)
        color = kwargs.get("color", self.color)
        timestamp = kwargs.get("timestamp", self.timestamp)
        footer = kwargs.get("footer", self.footer)
        image = kwargs.get("image", self.image)
        thumbnail = kwargs.get("thumbnail", self.thumbnail)
        author = kwargs.get("author", self.author)
        fields = kwargs.get("fields", self.fields)
        
        embed = Embed(
            title=title,
            description=description,
            url=url,
            color=color,
            timestamp=timestamp,
        )
        if footer and (footer.text or footer.icon_url):
            embed.set_footer(text=footer.text, icon_url=footer.icon_url)
        if image:
            embed.set_image(url=image)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        if author and (author.name or author.url or author.icon_url):
            embed.set_author(name=author.name, url=author.url, icon_url=author.icon_url)
        if fields:
            for field in fields:
                embed.add_field(name=field.name, value=field.value, inline=field.inline)
        return embed
       
        
    def format(
        self, 
        to_xembed : bool = False,
        use_cache : bool = True,
        **kwargs
    ):
        title = self._format(self.title, "title", self.extras, **kwargs)
        description = self._format(self.description, "description", self.extras, **kwargs)
        url = self._format(self.url, "url", self.extras, **kwargs)
        timestamp = self._format(self.timestamp, "timestamp", self.extras, **kwargs)
        image = self._format(self.image, "image", self.extras, **kwargs)
        thumbnail = self._format(self.thumbnail, "thumbnail", self.extras, **kwargs)

        
        footer = None
        author = None
        fields = []
        if self.footer and (self.footer.text or self.footer.icon_url):
            footer = {}
            footer["text"] =self.footer._format(self.footer.text, "text", self.extras, **kwargs),
            footer["icon_url"] =self.footer._format(self.footer.icon_url, "icon_url", self.extras, **kwargs),

        if self.author and (self.author.name or self.author.url or self.author.icon_url):
            author = {}
            author["name"] =self.author._format(self.author.name, "name", self.extras, **kwargs),
            author["url"] =self.author._format(self.author.url, "url", self.extras, **kwargs),
            author["icon_url"] =self.author._format(self.author.icon_url, "icon_url", self.extras, **kwargs),


        if self.fields:
            for field in self.fields:
                fields.append(
                    {
                        "name":field._format(field.name, "name", self.extras, **kwargs),
                        "value":field._format(field.value, "value", self.extras, **kwargs),
                        "inline" : field.inline
                    }
                )

        
        xembed = xEmbed(
            title=title,
            description=description,
            url=url,
            color=self.color,
            timestamp=timestamp,
            footer=footer,
            image=image,
            thumbnail=thumbnail,
            author=author,
            fields=fields,
        )
        if use_cache:
            self._handleCache(xembed, kwargs)
        
        if not to_xembed:
            return xembed.toEmbed()
            
        return xembed

    def _handleCache(self, w : 'xEmbed', kwargs :dict):
        if self.cache is None:
            return
        
        uid = str(uuid4())
        w.footer = xFooter(text=uid)
        self.cache[uid] = kwargs
        
    @cached_property
    def extraDefaults(self) -> typing.Dict[str, typing.Any]:
        defs = {}
        for k, v in self.vars.items():
            if v.default is None:
                continue
            defs[k] = v.default
            
        return defs             
   
   
    def parse(self, embed : Embed,use_cache_footer : bool = False):
        if use_cache_footer and embed.footer is not None:
            uid = embed.footer.text
            return self.cache[uid]    
        
        res = {}
        
        res = parseVars(self.title, embed.title, self.vars.get("title", None), res)
        res = parseVars(self.description, embed.description, self.vars.get("description", None), res)
        res = parseVars(self.url, embed.url, self.vars.get("url", None), res)
        res = parseVars(self.image, embed.image.url, self.vars.get("image", None), res)
        res = parseVars(self.thumbnail, embed.thumbnail.url, self.vars.get("thumbnail", None), res)
        res = parseVars(self.timestamp, embed.timestamp, self.vars.get("timestamp", None), res)
        
        if embed.footer:
            res = parseVars(self.footer.text, embed.footer.text, self.vars.get("footer", None), res)
            res = parseVars(self.footer.icon_url, embed.footer.icon_url, self.vars.get("footer", None), res)
        
        if embed.author:
            res = parseVars(self.author.name, embed.author.name, self.vars.get("author", None), res)
            res = parseVars(self.author.url, embed.author.url, self.vars.get("author", None), res)
            res = parseVars(self.author.icon_url, embed.author.icon_url, self.vars.get("author", None), res)
        
        if embed.fields:
            for field in embed.fields:
                res = parseVars(self.fields[0].name, field.name, self.vars.get("fields", None), res)
                res = parseVars(self.fields[0].value, field.value, self.vars.get("fields", None), res)
        
        return res

        
        
    

            

    