from discord.embeds import Embed
from discordPyExt.interfaces.embedColor import EmbedColor
from discordPyExt.utils.str import get_format_vars, format_string

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

        self.title_vars = get_format_vars(title)
        self.description_vars = get_format_vars(description)
        
        self.fields = []
        
    def field(self,
        name : str = None,
        value :str = None,
        inline : bool = False
    ):
        self.fields.append([{
            'name': name,
            'value': value,
            'inline': inline
        }, 
        {
            "name" : get_format_vars(name),
            "value" : get_format_vars(value)
        }]
        )
        return self

    
    def build(self, **kwargs):
        """
        build the embed
        """
        
        self.init_kwargs["title"] = format_string(self.init_kwargs["title"], **kwargs, format_vars=self.title_vars)
        self.init_kwargs["description"] = format_string(self.init_kwargs["description"], **kwargs, format_vars=self.description_vars)
        
        embed = EmbedX(**self.init_kwargs)

        for field in self.fields:
            field_vars, field_formats = field
            
            embed.add_field(
                name = format_string(field_vars["name"], **kwargs, format_vars=field_formats["name"]),
                value = format_string(field_vars["value"], **kwargs, format_vars=field_formats["value"]),
                inline = field_vars["inline"]
            )
            
        return embed