import pytest
from synchronized import synchronized, AutoSynchronized

def test_decorator():
    class TestClass:
        @synchronized
        def awesome_method(self):
            return "ok"

    tc = TestClass()
    assert hasattr(tc, "_auto_lock") == False
    assert tc.awesome_method() == "ok"
    assert hasattr(tc, "_auto_lock")


def test_metaclass():
    class TestClass:
        __metaclass__ = AutoSynchronized

        def awesome_method(self):
            return "ok"

    tc = TestClass()
    assert hasattr(tc, "_auto_lock")
    assert tc.awesome_method() == "ok"
    assert tc.synchronized_awesome_method() == "ok"
