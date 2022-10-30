
import shutil
from discordPyExt.ext.testCase import TestCaseX
from discordPyExt.setup import DcDeployer
from discordPyExt.setup.ext import DeployFlask, DeployReplitFlaskColdTrigger, DeployFlaskSQLAlchemy

class t_setup(TestCaseX):
    def test_can_deploy(self):
        """
        this tests if the deployer can be properly initialized
        """
        
        dp = DcDeployer(
            extensions=[DeployFlask, DeployReplitFlaskColdTrigger, DeployFlaskSQLAlchemy],
            path="test_data/setup",
            config_path="test_data/config",
            setup_mode=True,
            no_abort=True
        )
        with open("test_data/config/config.py", "w") as f:
            f.write("COLD_TRIGGER_SECRET='abcde'")
        
        import json
        with open("test_data/config/config.json", "r") as f:
            json_data = json.load(f)
        
        json_data["DISCORD_TOKEN"] = "test"
        json_data["COLD_TRIGGER_SECRET"] = "12345"
        with open("test_data/config/config.json", "w") as f:
            json.dump(json_data, f)    
    
        dp = DcDeployer(
            extensions=[DeployFlask, DeployReplitFlaskColdTrigger, DeployFlaskSQLAlchemy],
            path="test_data/setup",
            config_path="test_data/config",
            # in memory
            SQLALCHEMY_DATABASE_URI = "sqlite://",
        )
        
        driver = dp.config.getDriver("DISCORD_TOKEN")
        cold_trigger_key = dp.config.get("COLD_TRIGGER_SECRET")
        
        cold_trigger_key_from_json = dp.config.getDriver("DISCORD_TOKEN").get("COLD_TRIGGER_SECRET")
        
        self.assertEqual(driver["DISCORD_TOKEN"], "test")
        self.assertEqual(cold_trigger_key, "abcde")
        self.assertEqual(cold_trigger_key_from_json, "12345")
        
        pass
        
    def tearDown(self) -> None:
        shutil.rmtree("test_data/")