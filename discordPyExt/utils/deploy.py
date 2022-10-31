from discordPyExt.setup.deploy import DcDeployer, Storage, DataLoader
import click
# entry point function
import os
from discordPyExt.setup.ext import DeployFlask, DeployFlaskSQLAlchemy, DeployReplitFlaskColdTrigger
from discordPyExt.setup.extension import DcExtension
from discordPyExt.utils.misc import import_objs
import shutil

def _deploy(name, flask_sqlalchemy, replit_flask_cold_trigger, flask, logging):
    # check this is path
    os.makedirs(os.path.join(os.getcwd(), name), exist_ok=True)
    
    # if not empty
    if os.listdir(os.path.join(os.getcwd(), name)):
        print("Folder is not empty")
        return

    print("Preparing Extensions...")
    extensions = []
    additional_extensions = {}
    
    if flask:
        extensions.append(DeployFlask)
    
    if flask_sqlalchemy:
        extensions.append(DeployFlaskSQLAlchemy)
        
    if replit_flask_cold_trigger:
        extensions.append(DeployReplitFlaskColdTrigger)  
    
    # also check local ext folder for extensions
    print("Checking local extensions...")
    if os.path.exists(os.path.join(os.getcwd(), "ext")):
        for obj, filename in import_objs(f"ext", target=DcExtension, yield_file_name=True, only_type=True, only_object=False):
            print(f"Found extension {obj.__name__} in {filename}")
            extensions.append(obj)
            additional_extensions[filename] = obj
    
    # create a deployer
    print("Creating deployer...")
    DcDeployer(
        extensions=extensions,
        path=os.path.join(os.getcwd(), name),
        storage=Storage(),
        config=DataLoader.create_default(os.path.join(os.getcwd(), name)),
        setup_mode=True,
        no_abort=True
    )

    # copy all files in ext folder into the path
    print("Copying extension files...")
    if len(additional_extensions) > 0:
        os.makedirs(os.path.join(os.getcwd(), name, "ext"), exist_ok=True)
        for file in os.listdir(os.path.join(os.getcwd(),"ext")):
            if file.endswith(".py"):
                shutil.copy(os.path.join(os.getcwd(), "ext", file), os.path.join(os.getcwd(), name, "ext", file))

    
    # writes main file
    print("Writing main file...")
    with open(os.path.join(os.getcwd(), "main.py"), "w") as f:
        if logging:
            f.write("import logging, sys\n")
            f.write("logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)\n")
            
        f.write("from discordPyExt.setup import DcDeployer\n")
        if flask:
            f.write("from discordPyExt.setup.ext import DeployFlask\n")
        if flask_sqlalchemy:
            f.write("from discordPyExt.setup.ext import DeployFlaskSQLAlchemy\n")
            
        if replit_flask_cold_trigger:
            f.write("from discordPyExt.setup.ext import DeployReplitFlaskColdTrigger\n")
            
        for filename, extension in additional_extensions.items():
            f.write(f"from {name}.ext.{os.path.splitext(filename)[0]} import {extension.__name__}\n")
        
        f.write(f"from {name}.shared import config, storage\n")
        
        f.write("deployer = DcDeployer(\n")
        f.write("    extensions=[\n")
        for extension in extensions:
            f.write(f"        {extension.__class__.__name__},\n")
        f.write("    ],\n")
        f.write(f"    path='{name}',\n")
        f.write("    storage=storage,\n")
        f.write("    config=config,\n")
        f.write(")\n")

        
        print("Deployed successfully")

@click.command()
@click.argument("name", type=str)
# flag for extensions
@click.option("--flask-sqlalchemy", "-sql", is_flag=True)
@click.option("--replit-flask-cold-trigger", "-r", is_flag=True)
@click.option("--flask", "-f", is_flag=True)
# logging flag
@click.option("--logging", "-l", is_flag=True)
def deploy(name, flask_sqlalchemy, replit_flask_cold_trigger, flask, logging):
    _deploy(name, flask_sqlalchemy, replit_flask_cold_trigger, flask, logging)