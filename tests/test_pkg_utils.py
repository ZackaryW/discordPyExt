from discordPyExt.ext.testCase import TestCaseX
from discordPyExt.utils.str import get_format_vars

class utils(TestCaseX):
    def test_1(self):
        input = "hello, {user:str}"
        
        output = get_format_vars(input)
          
        self.assertEqual(output, {"user" : str})
        
    def test_2(self):
        input = "hello, {user}"
        
        output = get_format_vars(input)
          
        self.assertEqual(output, ["user"])
        
    def test_3(self):
        with self.assertRaises(ValueError):
            input = "hello, {user"
            
            output = get_format_vars(input)
              
            self.assertEqual(output, ["user"])
            
        with self.assertRaises(ValueError):
            input = "hello, user}"
            
            output = get_format_vars(input)
              
            self.assertEqual(output, ["user"])
            
        with self.assertRaises(ValueError):
            input = "hello, {{{user {}}"
            
            output = get_format_vars(input)