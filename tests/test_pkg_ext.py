import os
import shutil
from discordPyExt.ext import TestCaseX, DataLoader

class t_config(TestCaseX):
    def test_1(self):
        os.makedirs("test_data", exist_ok=True)
        with open("test_data/config.py", "w") as f:
            f.write("apple = 1\n")
            f.write("banana = 'orange'\n")
        
        x = DataLoader.create_default("test_data")
        
        self.assertEqual(x.apple, 1)
        self.assertEqual(x.banana, "orange")

        with self.assertRaises(AttributeError):
            x.noDupSet("apple", 2)
        
        x.noDupSet("orange", 3)    
        
        with open("test_data/config.py", "r") as f:
            self.assertEqual(f.read(), "apple = 1\nbanana = 'orange'\n")
        
        with open("test_data/config.json", "r") as f:
            self.assertEqual(f.read(), '{"orange":3}')
            
        
    # finally, delete the test data
    def tearDown(self):
        shutil.rmtree("test_data")