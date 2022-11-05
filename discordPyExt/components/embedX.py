from types import MappingProxyType
from discord.embeds import Embed
from discordPyExt.interfaces.embedColor import EmbedColor
from discordPyExt.utils.str import get_format_vars, format_string
import parse
import typing
import copy

class EmbedX(EmbedColor,Embed):
    pass

class EmbedFactory:
    """
    a factory class for creating embeds
    
    example:
    ```py
    factory = EmbedFactory(
        title = "Hello {name}",
        description = "This is a description"
    ).field(
        name = "Field 1",
        value = "Select {option} option"
    )
    
    embed = factory.build(name="World", option="this")
    ```
    
    """
    
    def __init__(self,
        colour = None,
        color= None,
        title= None,
        type = 'rich',
        url = None,
        description = None,
        timestamp = None,
        image=None,
        thumbnail=None,
    ) -> None:
        self.init_kwargs = {
            'colour': colour,
            'color': color,
            'title': title,
            'type': type,
            'url': url,
            'description': description,
            'timestamp': timestamp
        }

        self._image = image
        self._thumbnail = thumbnail

        self.fvar_positional_index = {}
        
        self.title_vars = get_format_vars(title)

        for var in self.title_vars:
            self.fvar_positional_index[var] = ["TITLE"]
        
        self.description_vars = get_format_vars(description)
        
        for var in self.description_vars:
            if var in self.fvar_positional_index:
                self.fvar_positional_index[var].append("DESCRIPTION")
            else:
                self.fvar_positional_index[var] = ["DESCRIPTION"]
        
        self.fields = []
        
    def field(self,
        name : str = None,
        value :str = None,
        inline : bool = False
    ):
        name_vars = get_format_vars(name)
        value_vars = get_format_vars(value)
        
        self.fields.append([{
            'name': name,
            'value': value,
            'inline': inline
        }, 
        {
            "name" :  name_vars,
            "value" : value_vars
        }]
        )
    
        for var in name_vars:
            if var in self.fvar_positional_index:
                self.fvar_positional_index[var].append(("FIELD_NAME", len(self.fields) - 1))
            else:
                self.fvar_positional_index[var] = [("FIELD_NAME", len(self.fields) - 1)]
        
        for var in value_vars:
            if var in self.fvar_positional_index:
                self.fvar_positional_index[var].append(("FIELD_VALUE", len(self.fields) - 1))
            else:
                self.fvar_positional_index[var] = [("FIELD_VALUE", len(self.fields) - 1)]
    
        return self

    
    def build(self, **kwargs):
        """
        build the embed
        """
        # if none 
        if self.init_kwargs["title"] is not None:
            title = format_string(self.init_kwargs["title"], **kwargs, format_vars=self.title_vars)
        else:
            title = None
        
        if self.init_kwargs["description"] is not None:
            description = format_string(self.init_kwargs["description"], **kwargs, format_vars=self.description_vars)
        else:
            description = None
        
        init_kwargs = {k: v for k, v in self.init_kwargs.items() if k != "title" and k != "description"}
        
        embed = EmbedX(
            title = title,
            description = description,
            **init_kwargs,
        )

        if self._image is not None:
            embed.set_image(url=self._image)
        
        if self._thumbnail is not None:
            embed.set_thumbnail(url=self._thumbnail)
        
        for field in self.fields:
            field_vars, field_formats = field
            
            embed.add_field(
                name = format_string(field_vars["name"], **kwargs, format_vars=field_formats["name"]),
                value = format_string(field_vars["value"], **kwargs, format_vars=field_formats["value"]),
                inline = field_vars["inline"]
            )
        
        #embed.__setattr__("_factory_init_kwargs", self.init_kwargs)
        #embed.__setattr__("_factory_fields", self.fields)
        
        return embed

    def _parse(self, format_str : str, format_vars : list, match_str : str):
        
        parsed = parse.parse(format_str, match_str)

        if parsed is not None:
            return parsed.named

        return None

    
    def _reparse_edit(self, format_str : str, format_vars : list, match_str : str, **kwargs):
        """
        example:
        format_str = "hello {str0}, this {str2} is an example of {str1}"
        match_str = "hello user, this 1 is an example of something"

        kwargs = {
            "str0" : "world",
            "str1" : "something else"
        }

        output = "hello world, this 1 is an example of something else"
        """
        
        if format_vars is not None and not any([var in format_vars for var in kwargs.keys()]):
            return match_str
        
        reparsed_data = self._parse(format_str, format_vars, match_str)

        if reparsed_data is None:
            return format_str.format(**kwargs)
    
        reparsed_data.update(kwargs)
        return format_str.format(**reparsed_data)

    
    def editEmbed(
        self, 
        embed: Embed,
        **kwargs
    ):
        """
        taking an embed and create a new embed with the same base data but with the new kwargs
        """
        title = self._reparse_edit(self.init_kwargs["title"], self.title_vars, embed.title, **kwargs)
        description = self._reparse_edit(self.init_kwargs["description"], self.description_vars, embed.description, **kwargs)
        
        fields = []
        for i, field in enumerate(self.fields):
            field_vars, field_formats = field
            embed_field = embed.fields[i]
            field = {
                'name': self._reparse_edit(field_vars["name"], field_formats["name"], embed_field.name, **kwargs),
                'value': self._reparse_edit(field_vars["value"], field_formats["value"], embed_field.value, **kwargs),
                'inline': field_vars["inline"]
            }
            fields.append(field)
        
        init_kwargs = {k: v for k, v in self.init_kwargs.items() if k != "title" and k != "description"}
        
        e =  EmbedX(
            title = title,
            description = description,  
            **init_kwargs,
        )

        for field in fields:
            e.add_field(
                name = field["name"],
                value = field["value"],
                inline = field["inline"]
            )
            
        return e
        
    
    def extractKey(self, embed: Embed, name: str):
        """
        extract the value of a key from an embed
        """

        if name not in self.fvar_positional_index:
            raise KeyError("key not found")
        
        # get first
        pos = self.fvar_positional_index[name][0]
        if pos == "TITLE":
            target = embed.title
            format_str = self.init_kwargs["title"]
        elif pos == "DESCRIPTION":
            target = embed.description
            format_str = self.init_kwargs["description"]
        elif pos[0] == "FIELD_NAME":
            target = embed.fields[pos[1]].name
            format_str = self.fields[pos[1]][0]["name"]
        elif pos[0] == "FIELD_VALUE":
            target = embed.fields[pos[1]].value
            format_str = self.fields[pos[1]][0]["value"]
        else:
            raise ValueError("invalid positional index")
        
        parsed = parse.parse(format_str, target)
        # setattr to embed 
        if parsed is None:
            return None
            
        return parsed.named[name]
    
    def extractKeys(self, embed: Embed):
        """
        extract all the keys from an embed
        """
        parsed = {}
        fvar_occurance = set()
        
        for val in self.fvar_positional_index.values():
            fvar_occurance.update(val)
            
        for pos in fvar_occurance:
            if pos == "TITLE":
                target = embed.title
                format_vars = self.title_vars
                format_str = self.init_kwargs["title"]
            elif pos == "DESCRIPTION":
                target = embed.description
                format_vars = self.description_vars
                format_str = self.init_kwargs["description"]
            elif pos[0] == "FIELD_NAME":
                target = embed.fields[pos[1]].name
                format_str = self.fields[pos[1]][0]["name"]
                format_vars = self.fields[pos[1]][1]["name"]
            elif pos[0] == "FIELD_VALUE":
                target = embed.fields[pos[1]].value
                format_str = self.fields[pos[1]][0]["value"]
                format_vars = self.fields[pos[1]][1]["value"]
            else:
                raise ValueError("invalid positional index")
            
            if target is None:
                continue
            
            tmp_parsed = self._parse(format_str, format_vars, target)       
            if tmp_parsed is None:
                continue
                
            
            parsed.update(tmp_parsed)

        
        return parsed
    
    def inherit(self,
        colour = None,
        color= None,
        title= None,
        type = None,
        url = None,
        description = None,
        timestamp = None,
        image = None,
        thumbnail = None,
    ):
        _copi = copy.deepcopy(self)
        # gather locals filter out none 
        vars = {
            k: v for k, v in locals().items() 
            if v is not None 
            and k not in ["self", "image", "thumbnail"] 
            and not k.startswith("_")
        }
        
        # update init_kwargs
        _copi.init_kwargs.update(vars)

        # if title changed
        if title is not None:
            _copi.title_vars = get_format_vars(title)

        if description is not None:
            _copi.description_vars = get_format_vars(description)
        
        _copi._image = image
        _copi._thumbnail = thumbnail
        
        return _copi