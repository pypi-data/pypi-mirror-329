
from typing import Union, override
from test._asset_loader_test import TestPythonAsset


class TestClass2(TestPythonAsset):
    def __init__(self):
        super().__init__()
        self.some_property = 'test 2'

    @override
    def some_method(self) -> Union[int, None]:
        return 2