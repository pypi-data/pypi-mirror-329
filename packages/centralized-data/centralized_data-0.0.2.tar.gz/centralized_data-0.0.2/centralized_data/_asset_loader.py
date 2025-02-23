from __future__ import annotations
from abc import ABC, abstractmethod
from json import loads
from os import getenv, path, walk
import sys
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from typing import Dict, List, Type, override

from yaml import safe_load
from ._singleton import Bindable

class LoadedAsset(ABC):
    """Asset loaded by the AssetLoader."""
    ...

class AssetLoader[T: LoadedAsset](Bindable):
    """
        Bindable that loads assets automatically. These assets are abstract.

        Currently there's 3 types of files that can be loaded below:
        * `.py` - PythonAssetLoader
        * `.yaml` - YamlAssetLoader
        * `.json` - JSONAssetLoader

        Do not use these classes directly, override them and make sure to implement
        the type T and the method `asset_folder_name`.

        Assets need to be located under a folder `*/assets/asset_folder_name/*`.

        You can override the Environment Variable `ASSET_LOADER_BASE_DIR` to change
        the base directory used to search the assets in case you're working on a
        large file system. If you're using a small system (e.g. via a simple Docker
        application), you don't need to necesserily adjust this variable.
    """
    loaded_assets: List[T]
    """Typed list of the loaded asset objects."""

    @override
    def constructor(self) -> None:
        super().constructor()
        self.loaded_assets: List[T] = []
        self.load_asset_modules()

    @abstractmethod
    def asset_folder_name(self) -> str:
        """
            This method must be overriden to find your assets.
        """
        ...
    @abstractmethod
    def asset_file_extension(self) -> str:
        """
            If you're implementing a loader for file type that's not pre-defined
            by this package, you will need to override this method.
        """
        ...
    @abstractmethod
    def load_asset(self, filename: str) -> None:
        """
            If you're implementing a loader for file type that's not pre-defined
            by this package, you will need to override this method.

            Once you instantiate your `T` object, add it using `self.add_asset()`
        """
        ...

    def add_asset(self, obj: T, name: str) -> None:
        """
            Add the asset to the asset list. Only call this method through `self.load_asset()`.
        """
        self.loaded_assets.append(obj)
        print(f"Asset {name} loaded by {self.__class__.__name__}.")

    def load_asset_modules(self) -> None:
        directory = self.asset_folder_name()
        base_directory = getenv("ASSET_LOADER_BASE_DIR") or "/"

        # Start from the root directory and search the whole filesystem
        for root, dirs, files in walk(base_directory):
            root =  root.replace('\\', '/')
            if "assets/" + directory in root:
                for file in files:
                    if file.endswith(self.asset_file_extension()):
                        self.load_asset(path.join(root, file))


class PythonAsset(LoadedAsset):
    """
        Represents a Python class from a file.

        If you need to define a base class for the assets, make sure to implement the classmethod
        `base_asset_class_name()`, returning it's class name. This prevents the AssetLoader from
        assuming that your base class needs to be loaded as an asset.
    """
    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls == PythonAsset: return
        if cls.__name__ == cls.base_asset_class_name(): return
        instance = cls()
        PythonAssetLoader.current_loader.add_asset(instance, cls.__name__)

    @classmethod
    def base_asset_class_name(cls): return 'PythonAsset'


class PythonAssetLoader[T: PythonAsset](AssetLoader[T]):
    """
        Loads Python classes deriving from PythonAsset.

        Override this class and define `asset_folder_name` for it to be useable.
    """
    current_loader: AssetLoader[T] = None

    @override
    def asset_file_extension(self) -> str:
        return '.py'

    @override
    def load_asset(self, filename):
        if PythonAssetLoader.current_loader is not None:
            raise Exception("Cannot load assets from multiple loaders at the same time.")

        module_path = Path(filename)
        module_name = module_path.stem  # Get filename without .py
        module_path = str(module_path.resolve())

        spec = spec_from_file_location(module_name, module_path)
        if spec and spec.loader:
            module = module_from_spec(spec)
            sys.modules[module_name] = module
            PythonAssetLoader.current_loader = self
            try:
                spec.loader.exec_module(module)
            finally:
                PythonAssetLoader.current_loader = None


class YamlAsset(LoadedAsset):
    """
        Represents the entirety of a YAML File.

        Access the properties of the object via the `source` property.
    """
    source: Dict

    def __init__(self, filename: str):
        self.source = safe_load(open(filename).read())
        if self.source is None:
            self.source = {}


class YamlAssetLoader[T: YamlAsset](AssetLoader[T]):
    """
        Loads YAML classes deriving from YamlAsset.

        Override this class, define `asset_folder_name` and `asset_class` for it to be useable.
    """
    def asset_class(self) -> Type[T]: return YamlAsset

    @override
    def asset_file_extension(self) -> str: return '.yaml'

    @override
    def load_asset(self, filename):
        yaml_asset = self.asset_class()(filename)
        self.add_asset(yaml_asset, f'{self.asset_class().__name__}[{Path(filename).stem}]')

class JSONAsset(LoadedAsset):
    """
        Represents the entirety of a JSON File.

        Access the properties of the object via the `source` property.
    """
    source: Dict

    def __init__(self, filename: str):
        self.source = loads(open(filename).read())
        if self.source is None:
            self.source = {}

class JSONAssetLoader[T: JSONAsset](AssetLoader[T]):
    """
        Loads JSON classes deriving from JSONAsset.

        Override this class, define `asset_folder_name` and `asset_class` for it to be useable.
    """
    def asset_class(self) -> Type[T]: return JSONAsset

    @override
    def asset_file_extension(self) -> str: return '.json'

    @override
    def load_asset(self, filename):
        yaml_asset = self.asset_class()(filename)
        self.add_asset(yaml_asset, f'{self.asset_class().__name__}[{Path(filename).stem}]')