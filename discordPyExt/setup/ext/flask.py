
import os
import flask
from discordPyExt.setup.extension import DcExtension
from threading import Thread

from discordPyExt.utils.misc import import_objs

class DeployFlask(DcExtension):
    _hash = "FLASK"
    
    def setup(self,
        FLASK_BLUEPRINTS_PATH : str = "fcogs",
    ) -> None:
        if not os.path.isabs(FLASK_BLUEPRINTS_PATH):
            FLASK_BLUEPRINTS_PATH = os.path.join(
                self._base.path,
                FLASK_BLUEPRINTS_PATH
            )
        
        os.makedirs(FLASK_BLUEPRINTS_PATH, exist_ok=True)

    def init(
        self,
        FLASK_HOST : str = "0.0.0.0",
        FLASK_NAME : str = "dc-flask-app",
        FLASK_PORT : int = 3000,
        FLASK_DEBUG : bool = False,
        FLASK_SECRET_KEY : str = None,
        FLASK_OTHER_CONFIG : dict = {},
        FLASK_BLUEPRINTS_PATH : str = "fcogs",
    ) -> None:
        self.flask_app = flask.Flask(FLASK_NAME)
        
        if FLASK_SECRET_KEY is not None:
            self.flask_app.secret_key = FLASK_SECRET_KEY
        
        # if not absolute path
        if not os.path.isabs(FLASK_BLUEPRINTS_PATH):
            FLASK_BLUEPRINTS_PATH = os.path.join(
                self._base.path,
                FLASK_BLUEPRINTS_PATH
            )
            
        if not os.path.exists(FLASK_BLUEPRINTS_PATH):
            raise ValueError(f"FLASK_BLUEPRINTS_PATH does not exist: {FLASK_BLUEPRINTS_PATH}")
            
        self.flask_app.config.update(FLASK_OTHER_CONFIG)

        # load blueprints
        for blueprint in import_objs(folder_path=FLASK_BLUEPRINTS_PATH, target=flask.Blueprint):
            blueprint : flask.Blueprint
            self.flask_app.register_blueprint(blueprint, url_prefix=f"/{blueprint.name}")
        
        # save config
        self.host = FLASK_HOST
        self.port = FLASK_PORT
        self.debug = FLASK_DEBUG
    def run(self):
        def run_flask():
            self.flask_app.run(
                host=self.host,
                port=self.port,
                debug=self.debug,
            )
            
        self.flask_thread = Thread(target=run_flask)
        
        self.flask_thread.start()
        
            
        
    