
from collections import OrderedDict
import datetime
from functools import cached_property
import typing
from pydantic import BaseModel, Field, validator
from pydantic.main import ModelMetaclass
from enum import Enum
from discord.ext import commands
import discord

class TextMappingTypes(Enum):

    
    BOLD = "**{text}**"
    ITALIC = "*{text}*"
    UNDERLINE = "__{text}__"
    STRIKE = "~~{text}~~"
    CODE = "`{text}`"
    CODE_BLOCK = "```{text}```"
    SPOILER = "||{text}||"
    USER_MENTION = "<@{text}>"
    CHANNEL_MENTION = "<#{text}>"
    ROLE_MENTION = "<@&{text}>"
    TIME = "<t:{text}>"
    TIME_RELATIVE = "<t:{text}:R>"
    TIME_SHORT = "<t:{text}:t>"
    
class TextMappingUtils:
    """
    i dont have a good idea for where to put this

    this is a collection of functions used to help parse and record text mappings
    """
    _prefixed : typing.Dict[str, str] = None
    _suffixed : typing.Dict[str, str] = None
    @classmethod
    def prefixed_list(cls):
        if cls._prefixed is not None:
            return cls._prefixed
        
        prefixes ={}
        for en in TextMappingTypes:
            prefixes[en.value.split("{")[0]] = en.name

        cls._prefixed = prefixes
        return prefixes

    @classmethod
    def suffixed_list(cls):
        if cls._suffixed is not None:
            return cls._suffixed
        
        suffixes = {}
        for en in TextMappingTypes:
            suffixes[en.name] = en.value.split("}")[1]

        cls._suffixed = suffixes
        return suffixes

    
    
class TextMeta(ModelMetaclass):
    """
    in case a Text object is passed as the text argument,
    the wrapper will be appended to the front of the wrapper list
    
    ? This is used to allow for nested Text objects while keeping upkeep to a minimum
    
    """
    def __call__(cls,*args, **kwargs):
        # check if text is passed as a Text object
        text = args[0]
        wrapper = args[1:]
        
        if text is None:
            #missing text
            raise ValueError("Missing text")
        
        if isinstance(text, (float, int, bool)):
            # convert to string
            text = str(text)
        
        if not isinstance(text, str):
            # text is a Text cls
            # append the wrapper in front 
            wrapper = list(text.wrapper) + list(wrapper)
            text = text.text
        
        return super().__call__(text, *wrapper)
    
class TextInterface(BaseModel, metaclass=TextMeta):
    class Config:
        # ignore cached_property
        keep_untouched = (cached_property,)
    
    text : str
    wrapper : typing.List[TextMappingTypes] = Field(default_factory=list, unique_items=True)
    
    @validator("wrapper", pre=True)
    def _check_wrapper(cls, wrapper):
        wrapper = list(wrapper)
        for i, w in enumerate(wrapper):
            if isinstance(w, TextMappingTypes):
                continue
            elif isinstance(w, str):
                wrapper[i] = TextMappingTypes[w.upper()]
                
        wrapper = OrderedDict.fromkeys(wrapper)
        return list(wrapper)
    
    @property
    def _time_case(self):
        has_time = TextMappingTypes.TIME in self.wrapper 
        has_time_relative = TextMappingTypes.TIME_RELATIVE in self.wrapper
        has_time_short = TextMappingTypes.TIME_SHORT in self.wrapper
        
        time_cases = [has_time, has_time_relative, has_time_short].count(True)
    
        return time_cases
    
    def _check_compatible(self, wrapper):
        time_case =self._time_case
        if time_case > 1:
            raise TypeError("Text cannot have more than one time type")
        
        #has_spoiler = TextMappingTypes.SPOILER in wrapper
        #has_code = TextMappingTypes.CODE in wrapper
        has_code_block = TextMappingTypes.CODE_BLOCK in wrapper
        # check codeblock must be outermost (so last in list)
        if has_code_block and wrapper[-1] != TextMappingTypes.CODE_BLOCK:
            raise TypeError("Codeblock must be outermost wrapper")

        # there can be only one mention type
        has_user_mention = TextMappingTypes.USER_MENTION in wrapper
        has_channel_mention = TextMappingTypes.CHANNEL_MENTION in wrapper
        has_role_mention = TextMappingTypes.ROLE_MENTION in wrapper
        
        mention_cases = [has_user_mention, has_channel_mention, has_role_mention].count(True)
        
        if mention_cases > 1:
            raise TypeError("Text cannot have more than one mention type")
        
        if mention_cases > 0 and time_case > 0:
            raise TypeError("Text cannot have time and mention type")
        
        
    def _create_formatted_text(self, text, wrapper):
        if len(wrapper) == 0:
            return text
        
        self._check_compatible(wrapper)
        
        _text = text
        
        for en in wrapper:
            _text = en.value.format(text=_text)
        return _text
    
        
    def __init__(self, text, *keys) -> None:
        super().__init__(text=text, wrapper=keys)
    
    @classmethod    
    def Bold(cls, text: str):
        return cls(text, TextMappingTypes.BOLD)
    
    @classmethod
    def Italic(cls, text: str):
        return cls(text, TextMappingTypes.ITALIC)    

    @classmethod
    def Underline(cls, text: str):
        return cls(text, TextMappingTypes.UNDERLINE)
    
    @classmethod
    def Strike(cls, text: str):
        return cls(text, TextMappingTypes.STRIKE)
    
    @classmethod
    def Code(cls, text: str):
        return cls(text, TextMappingTypes.CODE)

    @classmethod
    def CodeBlock(cls, text: str):
        return cls(text, TextMappingTypes.CODE_BLOCK)
    
    @classmethod
    def Spoiler(cls, text: str):
        return cls(text, TextMappingTypes.SPOILER)
    
    @classmethod
    def UserMention(cls, text: str):
        return cls(text, TextMappingTypes.USER_MENTION)

    @classmethod
    def ChannelMention(cls, text: str):
        return cls(text, TextMappingTypes.CHANNEL_MENTION)
    
    @classmethod
    def RoleMention(cls, text: str):
        return cls(text, TextMappingTypes.ROLE_MENTION)
    
    @classmethod
    def Time(cls, text: str):
        return cls(text, TextMappingTypes.TIME)
    
    @classmethod
    def TimeRemaining(cls, text: str):
        return cls(text, TextMappingTypes.TIME_RELATIVE)

    @classmethod
    def TimeShort(cls, text: str):
        return cls(text, TextMappingTypes.TIME_SHORT)
    
    
    @classmethod
    def Now(cls):
        return cls(int(datetime.datetime.utcnow().timestamp()), TextMappingTypes.TIME)
    
    @classmethod
    def fromRaw(cls, text:str):
        """ parse based on TextMappingTypes
        
        for example:
        
        if text = "**||hello||**"

        then parse the result as
        
        text = hello
        wrapper = [TextMappingTypes.SPOILER, TextMappingTypes.BOLD]
        
        """
        wrapper = []
        empty_loop = False
        while True:
            if empty_loop:
                break
            empty_loop = True
            for prefix, key in TextMappingUtils.prefixed_list().items():
                suffix = TextMappingUtils.suffixed_list()[key]
                if text.startswith(prefix) and text.endswith(suffix):
                    text = text[len(prefix):-len(TextMappingUtils.suffixed_list()[key])]
                    wrapper.insert(0,TextMappingTypes[key])
                    empty_loop = False
                    break
                    
        return cls(text, *wrapper)

    def toDiscordObject(self, query_object: typing.Union[discord.Client, discord.Guild]= None):
        if not self.text.isnumeric():
            raise TypeError("Text must be numeric")
        
        self._check_compatible(self.wrapper)
        
        if query_object is None:
            return discord.Object(int(self.text))
        
        if TextMappingTypes.USER_MENTION in self.wrapper:
            return query_object.get_user(int(self.text))
    
        if TextMappingTypes.CHANNEL_MENTION in self.wrapper:
            return query_object.get_channel(int(self.text))
        
        if TextMappingTypes.ROLE_MENTION in self.wrapper and isinstance(query_object, discord.Guild):
            return query_object.get_role(int(self.text))
        
        if self._time_case > 0:
            return datetime.datetime.fromtimestamp(int(self.text))
    
    
    async def toDiscordObjectAsync(self, query_obj : typing.Union[discord.Client, discord.Guild] = None):
        res = self.toDiscordObject(query_obj)
        if res is not None:
            return res
        
        if TextMappingTypes.USER_MENTION in self.wrapper:
            return await query_obj.fetch_user(int(self.text))
        
        if TextMappingTypes.CHANNEL_MENTION in self.wrapper:
            return await query_obj.fetch_channel(int(self.text))
        
    
    
class Text(TextInterface):
    def __genericAdd(self, typ : TextMappingTypes):
        self.__dict__.pop("_tostr", None)
        if typ in self.wrapper:
            return
        self.wrapper.append(typ)
    
    def addBold(self) -> str:
        self.__genericAdd(TextMappingTypes.BOLD)
        return self
        
    def addItalic(self) -> str:
        self.__genericAdd(TextMappingTypes.ITALIC)
        return self
    
    def addUnderline(self) -> str:
        self.__genericAdd(TextMappingTypes.UNDERLINE)
        return self
        
    def addStrike(self) -> str:
        self.__genericAdd(TextMappingTypes.STRIKE)
        return self
    
    def addCode(self) -> str:
        self.__genericAdd(TextMappingTypes.CODE)
        return self
    
    def addCodeBlock(self) -> str:
        self.__genericAdd(TextMappingTypes.CODE_BLOCK)
        return self

    def addSpoiler(self) -> str:
        self.__genericAdd(TextMappingTypes.SPOILER)
        return self
    
    @cached_property
    def _tostr(self) -> str:
        return self._create_formatted_text(self.text, self.wrapper)
        
    def __str__(self) -> str:
        return self._tostr
    
    def __repr__(self) -> str:
        return self._tostr


    def __setattr__(self, __name: str, __value) -> None:
        if __name.startswith("_"):
            super().__setattr__(__name, __value)
            return
        
        if __name in ("text", "wrapper"):
            self.__dict__.pop("_tostr", None)
            
        super().__setattr__(__name, __value)
        

class ImmutableText(TextInterface):
    
    
    class Config:
        allow_mutation = False
        frozen = True
        keep_untouched = (cached_property,)
    
        
    def __str__(self) -> str:
        return self._tostr
    
    def __repr__(self) -> str:
        return self._tostr
        
    @cached_property
    def _tostr(self) -> str:
        return self._create_formatted_text(self.text, self.wrapper)
    
