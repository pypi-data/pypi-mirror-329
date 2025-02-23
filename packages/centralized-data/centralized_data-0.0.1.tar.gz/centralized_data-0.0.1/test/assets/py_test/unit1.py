
from typing import Union, override
from test._asset_loader_test import TestPythonAsset


class TestClass1(TestPythonAsset):
    def __init__(self):
        super().__init__()
        self.some_property = 'test 1'

    @override
    def some_method(self) -> Union[int, None]:
        return 1