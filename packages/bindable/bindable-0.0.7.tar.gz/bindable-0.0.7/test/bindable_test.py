import unittest

from src.bindable import Bindable

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

if __name__ == "__main__":
    unittest.main()