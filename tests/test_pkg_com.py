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
    def setUp(self) -> None:
        self.f = EmbedFactory(
            title="hello, {user}",
            description="hello, {server}",
        ).field(
            name="{user}, please read the rules",
            value="1. {user} is not allowed to do {action}",
        )    

    def test_1(self):
        
        embed = self.f.build(
            user="test",
            server="test",
            action="testaction",
        )
        
        self.assertEqual(embed.title, "hello, test")
        self.assertEqual(embed.description, "hello, test")
        self.assertEqual(embed.fields[0].name, "test, please read the rules")
        self.assertEqual(embed.fields[0].value, "1. test is not allowed to do testaction")
        
        embed2 = self.f.editEmbed(
            embed=embed,
            user="test2",
            server="test2",
            action="testaction2",
        ) 
        
        self.assertEqual(embed2.title, "hello, test2")
        self.assertEqual(embed2.description, "hello, test2")
        self.assertEqual(embed2.fields[0].name, "test2, please read the rules")
        self.assertEqual(embed2.fields[0].value, "1. test2 is not allowed to do testaction2")

        val = self.f.extractKey(
            embed=embed2,
            name="action",
        )

        self.assertEqual(val, "testaction2")