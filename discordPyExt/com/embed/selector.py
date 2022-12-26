from discord import Embed

class xEmbedColorSelector:
    """
    helps to select color for embeds
    """
    
    def __init__(self, embed : Embed) -> None:
        self.embed = embed
        
    def red(self):
        self.embed.color = 0xff0000
        return self.embed
    
    def green(self):
        self.embed.color = 0x00ff00
        return self.embed
    
    def blue(self):
        self.embed.color = 0x0000ff
        return self.embed
    
    def yellow(self):
        self.embed.color = 0xffff00
        return self.embed
    
    def cyan(self):
        self.embed.color = 0x00ffff
        return self.embed
    
    def magenta(self):
        self.embed.color = 0xff00ff
        return self.embed
    
    def black(self):
        self.embed.color = 0x000000
        return self.embed

class xEmbedStatusSelector:
    """
    helps to create quick embeds with status
    """
    
    def __init__(self, embed : Embed) -> None:
        self.embed = embed
    
    def success(self):
        self.embed.color = 0x00ff00
        return self.embed
    
    def error(self):
        self.embed.color = 0xff0000
        return self.embed
    
    def warning(self):
        self.embed.color = 0xffff00
        return self.embed
    
    def info(self):
        self.embed.color = 0x0000ff
        return self.embed