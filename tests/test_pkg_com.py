from discordPyExt.components.text import Text, ImmutableText, TextMappingTypes
from discordPyExt.ext.testCase import TestCaseX

class text(TestCaseX):
    def test_1(self):
        with self.profiler(print_stats=True):
        
            x = ImmutableText("test", TextMappingTypes.BOLD, TextMappingTypes.ITALIC, TextMappingTypes.CODE)
            # print markdown
            print(x)
        
        pass
        
        with self.profiler(print_stats=True):
        
            y = ImmutableText.Code(ImmutableText.Italic(ImmutableText.Bold("test")))
            print(y)
        
        pass
    
    def test_2(self):
        text = "||**__*`hello`*__**||"
        x = Text.fromRaw(text)
        self.assertEqual(str(x), text)
        pass
    
from discordPyExt import EmbedFactory

class t_embed_factory(TestCaseX):
    def test_1(self):
        f = EmbedFactory(
            title="hello, {user}",
            description="hello, {server}",
        ).field(
            name="{user}, please read the rules",
            value="1. {user} is not allowed to do {action}",
        )

        embed = f.build(
            user="test",
            server="test",
            action="testaction",
        )
        pass