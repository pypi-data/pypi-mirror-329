from os import environ
from pathlib import Path
from typing import Type, Union, override
import unittest
from centralized_data import LoadedAsset, AssetLoader, YamlAsset, YamlAssetLoader, JSONAsset, JSONAssetLoader, PythonAsset, PythonAssetLoader

class TestTXTAsset(LoadedAsset):
    content: str

    def __init__(self, filename: str):
        self.content = open(filename).read()
        if self.content is None:
            self.content = ''

class TestTXTAssetLoader(AssetLoader[TestTXTAsset]):
    def asset_class(self) -> Type[TestTXTAsset]: return TestTXTAsset

    @override
    def asset_file_extension(self) -> str: return '.txt'

    @override
    def load_asset(self, filename):
        txt_asset = self.asset_class()(filename)
        path = Path(filename)
        self.add_asset(txt_asset, f'{self.asset_class().__name__}[{path.stem}]')

    @override
    def asset_folder_name(self):
        return 'txt_test'

class TestYamlAsset(YamlAsset):
    @property
    def name(self) -> str:
        return self.source.get("name", "no-name")

class TestYamlAssetLoader(YamlAssetLoader[TestYamlAsset]):
    def asset_class(self) -> Type[TestYamlAsset]: return TestYamlAsset
    @override
    def asset_folder_name(self):
        return 'yaml_test'

class TestJSONAsset(JSONAsset):
    @property
    def name(self) -> str:
        return self.source.get("name", "no-name")

class TestJSONAssetLoader(JSONAssetLoader[TestJSONAsset]):
    def asset_class(self) -> Type[TestJSONAsset]: return TestJSONAsset
    @override
    def asset_folder_name(self):
        return 'json_test'

class TestPythonAsset(PythonAsset):
    some_property: str
    @classmethod
    def base_asset_class_name(cls): return 'TestPythonAsset'

    def some_method(self) -> Union[int, None]:
        return None

class TestPythonAssetLoader(PythonAssetLoader[TestPythonAsset]):
    @override
    def asset_folder_name(self):
        return 'py_test'

class TestMain(unittest.TestCase):
    def test_txt(self):
        environ["ASSET_LOADER_BASE_DIR"] = 'D:\\workspaces\\py-centralized_data\\test'
        assets = TestTXTAssetLoader().loaded_assets
        self.assertEqual(len(assets), 2, 'Failed to load all assets.')
        self.assertEqual(assets[0].content, 'hello world', 'assets[0] file content')
        self.assertEqual(assets[1].content, 'world hello', 'assets[1] file content')

    def test_yaml(self):
        environ["ASSET_LOADER_BASE_DIR"] = 'D:\\workspaces\\py-centralized_data\\test'
        assets = TestYamlAssetLoader().loaded_assets
        self.assertEqual(len(assets), 2, 'Failed to load all assets.')
        self.assertEqual(assets[0].name, 'cool_yaml')
        self.assertEqual(assets[1].name, 'no-name')

    def test_json(self):
        environ["ASSET_LOADER_BASE_DIR"] = 'D:\\workspaces\\py-centralized_data\\test'
        assets = TestJSONAssetLoader().loaded_assets
        self.assertEqual(len(assets), 2, 'Failed to load all assets.')
        self.assertEqual(assets[0].name, 'cool_json')
        self.assertEqual(assets[1].name, 'no-name')

    def test_py(self):
        environ["ASSET_LOADER_BASE_DIR"] = 'D:\\workspaces\\py-centralized_data\\test'
        assets = TestPythonAssetLoader().loaded_assets
        self.assertEqual(len(assets), 2, 'Failed to load all assets.')
        self.assertEqual(assets[0].some_property, 'test 1', 'assets[0] some_property')
        self.assertEqual(assets[0].some_method(), 1, 'assets[0] some_method')
        self.assertEqual(assets[1].some_property, 'test 2', 'assets[1] some_property')
        self.assertEqual(assets[1].some_method(), 2, 'assets[1] some_method')

if __name__ == '__main__':
    unittest.main()