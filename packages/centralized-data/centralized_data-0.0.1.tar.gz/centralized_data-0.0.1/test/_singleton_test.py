from typing import override
import unittest

from centralized_data import Bindable, GlobalCollection

class BindableT(Bindable):
    def constructor(self, *a, **kw) -> None:
        super().constructor()
        self.some_value = kw.get('some_value')

    def method(self) -> str:
        return 'Success!'

class TestObject:
    @BindableT.bind
    def testbinding(self) -> BindableT: ...

class TestBindable(unittest.TestCase):
    def test_singletons(self):
        self.assertEqual(BindableT(some_value=3), BindableT(), 'Constructors return different objects.')
        self.assertEqual(BindableT().some_value, BindableT().some_value, 'Values arent equal.')
        self.assertEqual(BindableT(some_value=3).some_value, BindableT(some_value=4).some_value, 'Constructors are called multiple times.')
        BindableT().some_value = 4
        self.assertEqual(BindableT().some_value, 4, 'Value has not changed changed.')

    def test_binding(self):
        obj = TestObject()
        self.assertEqual(obj.testbinding, BindableT(), 'Binding != Bindable()')
        BindableT().some_value = 1
        self.assertEqual(obj.testbinding.some_value, 1, 'Access to value from binding')
        self.assertEqual(obj.testbinding.method(), 'Success!', 'Access to binding from method')

class GlobalCollectionT(GlobalCollection[int]):
    @override
    def constructor(self, key: int = None) -> None:
        super().constructor(key)
        self.some_property = 'testing ' + str(key or 0)

class TestGlobalCollection(unittest.TestCase):
    def test_elements(self):
        GlobalCollectionT.clear()
        self.assertEqual(GlobalCollectionT(1).some_property, 'testing 1')
        self.assertEqual(GlobalCollectionT(2).some_property, 'testing 2')
        self.assertEqual(GlobalCollectionT(3).some_property, 'testing 3')
        GlobalCollectionT(3).some_property = 'changed'
        self.assertEqual(GlobalCollectionT(3).some_property, 'changed')
        self.assertEqual(GlobalCollectionT().some_property, 'testing 0')

    def test_clear(self):
        GlobalCollectionT(10)
        GlobalCollectionT(11)
        GlobalCollectionT.clear()
        self.assertEqual(GlobalCollectionT.count(), 0)

    def test_pop(self):
        GlobalCollectionT.clear()
        GlobalCollectionT(1).some_property = 'something'
        GlobalCollectionT(1).pop()
        self.assertEqual(GlobalCollectionT.count(), 0)

if __name__ == "__main__":
    unittest.main()