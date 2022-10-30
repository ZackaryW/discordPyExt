
import flask
from discordPyExt.setup.extension import DcExtension
from flask_sqlalchemy import SQLAlchemy
from discordPyExt.setup.ext.flask import DeployFlask
from sqlalchemy.orm import declarative_base
import typing
import os
class DeployFlaskSQLAlchemy(DcExtension):
    def check_init(self):
        return self._base.isInit(DeployFlask)
        
    def check(self, 
        SQLALCHEMY_MODEL_FILE : str = "models",
    ):
        if SQLALCHEMY_MODEL_FILE is None:
            raise ValueError("declarative_base must be set")
        

        self.SQLALCHEMY_MODEL_FILE = SQLALCHEMY_MODEL_FILE
    
        # if not abs
        if not os.path.isabs(self.SQLALCHEMY_MODEL_FILE):
            # get abs path
            self.SQLALCHEMY_MODEL_FILE = os.path.join(self._base.path, self.SQLALCHEMY_MODEL_FILE)
                
        return super().check()
        
    def init(
        self,
        SQLALCHEMY_DATABASE_URI : str,
        SQLALCHEMY_TRACK_MODIFICATIONS : bool = False,
        SQLALCHEMY_ECHO : bool = False,
        SQLALCHEMY_BINDS : typing.Dict[str, str] = None,
        SQLALCHEMY_ENGINE_OPTIONS : typing.Dict[str, typing.Any] = None,
    ) -> None:
        
    
        # import model file
        model_package = self.SQLALCHEMY_MODEL_FILE.replace("/" , ".").replace("\\" , ".")
        # childest package
        child = model_package.split(".")[-1]
        
        base = __import__(model_package, fromlist=[child])
        # get base
        self.sql_declarative_base = base.base
        
        if SQLALCHEMY_DATABASE_URI is None:
            raise ValueError("SQLALCHEMY_DATABASE_URI must be set")
        
        self.flask_app : flask.Flask
        self.flask_app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
        self.flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
        self.flask_app.config["SQLALCHEMY_ECHO"] = SQLALCHEMY_ECHO
        
        if SQLALCHEMY_BINDS is not None:
            self.flask_app.config["SQLALCHEMY_BINDS"] = SQLALCHEMY_BINDS
        
        if SQLALCHEMY_ENGINE_OPTIONS is not None:
            self.flask_app.config["SQLALCHEMY_ENGINE_OPTIONS"] = SQLALCHEMY_ENGINE_OPTIONS
        
        self.flask_sql : SQLAlchemy = SQLAlchemy(self.flask_app)
        self.flask_sql.Model = self.sql_declarative_base
        
    def setup(
        self,
    ) -> None:
        # create model file at target location
        path = self.SQLALCHEMY_MODEL_FILE.replace("." , "/")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        if not os.path.exists(path):
        
            with open(path + ".py", "w") as f:
                f.write("from sqlalchemy.orm import declarative_base\n")
                f.write("from sqlalchemy import Column, Integer, String\n")
                f.write("base = declarative_base()\n")
                
                f.write("\n")
                # add example db
                f.write("class Example(base):\n")
                f.write("    __tablename__ = 'example'\n")
                f.write("    id = Column(Integer, primary_key=True)\n")
                f.write("    name = Column(String(50))\n")
                f.write("    value = Column(Integer)\n")

    def run(self):
        self.flask_sql.create_all()