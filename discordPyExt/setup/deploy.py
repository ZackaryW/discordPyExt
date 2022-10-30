
import asyncio
import logging
import os
import typing
import sys
from discordPyExt.ext.data import DataLoader
from discordPyExt.setup.extension import DcExtension
from discordPyExt.setup.interface import DcDeployerInterface
from discordPyExt.setup.ext.bot import DeployBot
import inspect

from discordPyExt.ext.storage import Storage
    
class DcDeployer(DcDeployerInterface):
    """
    a DcDeployer is an auto deployer for discord.py bots
    
    it supports the use of multiple extensions, and centralizes the setup process (and storage)
    """
    
    def _gather_needed_params(self, func : typing.Callable, **parameters : typing.Dict[str, typing.Any]) -> typing.Dict[str, inspect.Parameter]:
        """
        gathers needed parameters for a function
        
        Returns:
            typing.Dict[str, typing.Any]: a dict of parameters with default / existing config values
        """
        
        params_needed = inspect.signature(func).parameters
        params_needed = {k: v for k, v in params_needed.items() if k != "self"}
        
        # filter parameters
        params = {k: v for k, v in parameters.items() if k in params_needed}
            
        # get missing parameters
        params_needed = {k: v for k, v in params_needed.items() if k not in params}
        
        # get missing parameters from config
        for k, v in params_needed.items():
            params[k] = self.config.get(k, None)
            if params[k] is None and v.default is not inspect.Parameter.empty:
                params[k] = v.default
                
    
        return params
    
    def __init__(self, 
        extensions : typing.List[DcExtension],
        path : str,
        logger : logging.Logger =  logging.getLogger("DcDeployer"),
        config_path : str = "appdata",
        setup_mode : bool = False,
        setup_mode_check_sys_argv : bool = True,
        no_abort : bool = False,
        **parameters : typing.Dict[str, typing.Any]
    ) -> None:
        """
        initializes a DcDeployer
        
        Args:
            `extensions` (typing.List[DcExtension]): a list of extensions to load
            
            `path` (str): the path to store data in
            
            `logger` (logging.Logger, optional): the logger to use. Defaults to logging.getLogger("DcDeployer").
            
            `config_path` (str, optional): the path to store config in. Defaults to "appdata".
            
            `setup_mode` (bool, optional): whether to run in setup mode. Defaults to False.
            
            `setup_mode_check_sys_argv` (bool, optional): whether to check sys.argv for setup mode. Defaults to True.
            
            `no_abort` (bool, optional): whether to abort after setup. Defaults to False
        """
        # check extensions
        if any((
                not (
                    issubclass(arg, DcExtension) 
                    or isinstance(arg, DcExtension)
                )
                or (issubclass(arg, DeployBot) or isinstance(arg, DeployBot))
            ) for arg in extensions
        ):
            raise TypeError("All extensions must be a subclass of DcExtension and not a subclass of DeployBot")
        
        self.logger = logger
        self.no_abort = no_abort
        
        # check setup mode
        if setup_mode_check_sys_argv and len(sys.argv) > 1 and "--setup" in sys.argv:
            setup_mode = True
        
        self._on_init_params = parameters
        self.path = path
        self.config_path = config_path
        # make folder        
        os.makedirs(self.path, exist_ok=True)
        os.makedirs(self.config_path, exist_ok=True)
    
        # initilize loop
        self.loop = asyncio.get_event_loop()
        
        self.storage : Storage = Storage()

        # setup config
        self.config : DataLoader = DataLoader.create_default(
            path=config_path,
        )
        
        self.extension_configs :dict = {}
        
        self.config._add_non_driver(self.extension_configs)
        # setup deploy bot
        self._deploy_bot : DeployBot = DeployBot()
        self._deploy_bot._base = self
        
        self.extensions : typing.Dict[str,DcExtension] = {}
        
        # preprocess extensions
        for i, ext in enumerate(extensions):
            ext : DcExtension
            # make obj
            if ext._hash in self.extensions:
                self.logger.warning(f"Extension {ext} already loaded")
                continue
            
            # update config
            # make sure no keys already exist
            ext_configs = ext.configs()
            
            for k, v in ext_configs.items():
                if k in self.extension_configs:
                    raise KeyError(f"Key {k} already exists in extension configs")
                self.extension_configs[k] = v
            
            if isinstance(ext, type):
                ext = ext()     
            ext._base = self
            
            extensions[i] = ext
        
        if setup_mode:
            self.setup(*extensions)
        else:
            self.init(*extensions)
                

    def setup(self, *extensions : typing.List[DcExtension]):
        # set up deploy_bot
        params = self._gather_needed_params(self._deploy_bot.setup, **self._on_init_params)
        self._deploy_bot.setup(**params)
        
        for ext in extensions:
            check_params = self._gather_needed_params(ext.check, **self._on_init_params)
            if not ext.check(**check_params):
                raise RuntimeError(f"Extension {ext} failed check")
            
            check_setup_params = self._gather_needed_params(ext.check_setup, **self._on_init_params)
            if not ext.check_setup(**check_setup_params):
                raise RuntimeError(f"Extension {ext} failed setup check")    
            
            ext : DcExtension
            print("Setting up extension: " + ext.__class__.__name__)
            params= self._gather_needed_params(ext.setup, **self._on_init_params)
            ext.setup(**params)
            
        print("Setup complete")
        
        if self.no_abort:
            return
        os.abort()

    def init(self, *extensions : typing.List[DcExtension]):
        self._init_extension(self._deploy_bot,_no_append=True, **self._on_init_params)
        
        for ext in extensions:
            ext : DcExtension
            # make obj
            
            check_params = self._gather_needed_params(ext.check, **self._on_init_params)
            if not ext.check(**check_params):
                raise RuntimeError(f"Extension {ext} failed check")
                            
            self._init_extension(ext, **self._on_init_params)

    def _init_extension(self, ext : DcExtension, _no_append : bool = False ,**parameters : typing.Dict[str, typing.Any]):
        """
        initializes an extension
        """
        
        params = self._gather_needed_params(ext.init, **parameters)

        if not ext.check_init():
            raise Exception("Extension failed to init")
        
        # run init
        # check if coroutines
        if inspect.iscoroutinefunction(ext.init):
            self.loop.create_task(ext.init(**params))
            # run loop and wait for init to finish
            self.loop.run_until_complete(asyncio.sleep(0))
            
        else:
            ext.init(**params)
        
        if not _no_append:
            self.extensions[ext._hash] = ext

    def run(self):
        """
        runs the server
        """
        
        for ext in self.extensions:
            ext : DcExtension
            if inspect.iscoroutinefunction(ext.run):
                self.loop.create_task(ext.run())
                self.loop.run_until_complete(asyncio.sleep(0))
            else:
                ext.run()
        
        self._deploy_bot.run()
    
    def isInit(self, extension : DcExtension) -> bool:
        """
        checks if an extension is initialized
        
        Args:
            `extension` (DcExtension)
        """
        return extension._hash in self.extensions