import flask
from discordPyExt.setup.extension import DcExtension
from discordPyExt.setup.ext.flask import DeployFlask
import os
from flask import request


class DeployReplitFlaskColdTrigger(DcExtension):
    flask_app : flask.Flask
    
    def check_init(self):
        return self._base.isInit(DeployFlask)
        
    def init(
        self,
        COLD_TRIGGER_ROUTE : str = "COLD_TRIGGER",
        COLD_TRIGGER_SECRET : str = None,
    ) -> None:
        
        if COLD_TRIGGER_SECRET is None:
            raise ValueError("COLD_TRIGGER_SECRET must be set")
            
        def replit_coldtrigger():
            # get token
            token = request.headers.get("TOKEN")

            # check token
            if token != COLD_TRIGGER_SECRET:
                return "TOKEN MISMATCH", 403
            # 
            os.system("kill 1")
        
        # register cold trigger route
        self.flask_app.route(f"/{COLD_TRIGGER_ROUTE}")(replit_coldtrigger)

