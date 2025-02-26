"""
Test: Core

Version: 5.0.0
Date updated: 14/02/2025 (dd/mm/yyyy)
"""

from inspect import getdoc
from typing import Any

import pytest

from absfuyu import __version__
from absfuyu.core import BaseClass
from absfuyu.core.baseclass import AutoREPRMixin
from absfuyu.core.decorator import dummy_decorator, dummy_decorator_with_args
from absfuyu.core.docstring import (
    _SPHINX_DOCS_TEMPLATE,
    SphinxDocstring,
    SphinxDocstringMode,
)


class ClassToTestDocs:
    def method(self, *args, **kwargs):
        """Normal method"""
        pass

    @classmethod
    def cmethod(cls, *args, **kwargs):
        """classmethod"""
        pass

    @staticmethod
    def stmethod(*args, **kwargs):
        """staticmethod"""
        pass


@pytest.mark.abs_core
class TestBaseClass:
    """
    ``absfuyu.core.BaseClass``
    """

    def test_BaseClass(self) -> None:
        _ = BaseClass.show_all_methods(print_result=True)


@pytest.mark.abs_core
class TestAutoREPRMixin:
    """``absfuyu.core.core_class.AutoREPRMixin``"""

    def test_class_no_slots(self) -> None:
        class ClassNoSlots(AutoREPRMixin):
            def __init__(self, a) -> None:
                self.a = a

        instance = ClassNoSlots(1)
        name = instance.__class__.__name__
        expected = f"{name}(a={instance.a!r})"
        assert repr(instance) == expected

    def test_class_with_slots(self) -> None:
        class ClassWithSlots(AutoREPRMixin):
            __slots__ = ("a",)

            def __init__(self, a) -> None:
                self.a = a

        instance = ClassWithSlots(1)
        name = instance.__class__.__name__
        expected = f"{name}(a={instance.a!r})"
        assert repr(instance) == expected


@pytest.mark.abs_core
class TestCoreDecorator:
    def test_dummy_decorator(self) -> None:
        # Define a dummy function to decorate
        def add(a, b):
            return a + b

        # Apply the decorator
        decorated_add = dummy_decorator(add)

        # Test if the decorated function behaves as expected
        assert decorated_add(2, 3) == 5

    def test_dummy_decorator_class(self) -> None:
        # Define a class to decorate (which does nothing)
        class MyClass:
            pass

        # Apply the decorator to the class (should return unchanged)
        DecoratedClass = dummy_decorator(MyClass)

        assert DecoratedClass is MyClass

    def test_dummy_decorator_with_args(self) -> None:
        def multiply(a, b):
            return a * b

        decorator_instance = dummy_decorator_with_args("arg1", kwarg="value")

        decorated_multiply = decorator_instance(multiply)

        assert decorated_multiply(4, 5) == 20

    def test_dummy_decorator_with_args_class(self) -> None:
        class MyOtherClass:
            pass

        decorator_instance_for_class = dummy_decorator_with_args("arg1", kwarg="value")
        DecoratedOtherClass = decorator_instance_for_class(MyOtherClass)

        assert DecoratedOtherClass is MyOtherClass


@pytest.mark.abs_core
class TestSphinxDocstring:
    """
    ``absfuyu.core.SphinxDocstring``
    """

    @pytest.mark.parametrize(
        ["reason", "mode"],
        [
            (None, SphinxDocstringMode.ADDED),
            (None, SphinxDocstringMode.CHANGED),
            (None, SphinxDocstringMode.DEPRECATED),
            ("test", SphinxDocstringMode.ADDED),
            ("test", SphinxDocstringMode.CHANGED),
            ("test", SphinxDocstringMode.DEPRECATED),
        ],
    )
    def test_SphinxDocstring_function(
        self, reason: str | None, mode: SphinxDocstringMode
    ) -> None:
        # Create a function with decorator
        @SphinxDocstring(__version__, reason=reason, mode=mode)
        def demo_function(parameter: Any) -> Any:
            return parameter

        @SphinxDocstring(__version__, reason=reason, mode=mode)
        def demo_function_2(parameter: Any) -> Any:
            """This already has docs"""
            return parameter

        # Get template
        _reason = f": {reason}" if reason else ""
        template = _SPHINX_DOCS_TEMPLATE.substitute(
            line_break="",
            mode=mode.value,
            version=__version__,
            reason=_reason,
        )

        for func in [demo_function, demo_function_2]:
            # Get docstring
            docs: str = getdoc(func)
            # Assert
            assert docs.endswith(template)

    @pytest.mark.parametrize(
        ["reason", "mode"],
        [
            (None, SphinxDocstringMode.ADDED),
            (None, SphinxDocstringMode.CHANGED),
            (None, SphinxDocstringMode.DEPRECATED),
            ("test", SphinxDocstringMode.ADDED),
            ("test", SphinxDocstringMode.CHANGED),
            ("test", SphinxDocstringMode.DEPRECATED),
        ],
    )
    def test_SphinxDocstring_class(
        self, reason: str | None, mode: SphinxDocstringMode
    ) -> None:
        @SphinxDocstring(__version__, reason=reason, mode=mode)
        class KlassNoDoc(ClassToTestDocs): ...

        @SphinxDocstring(__version__, reason=reason, mode=mode)
        class KlassWithDoc(ClassToTestDocs):
            """
            This is a doc
            """

            pass

        @SphinxDocstring(__version__, reason=reason, mode=mode)
        class SubClass(KlassNoDoc): ...

        test_list: list[ClassToTestDocs] = [KlassNoDoc, KlassWithDoc, SubClass]
        for k in test_list:
            docs: str = getdoc(k)  # Get docstring
            _reason = f": {reason}" if reason else ""
            template = _SPHINX_DOCS_TEMPLATE.substitute(
                line_break="",
                mode=mode.value,
                version=__version__,
                reason=_reason,
            )  # Retrive template str

            to_test = all(
                [
                    k.__doc__.endswith(template),
                    k().__doc__.endswith(template),
                    k.cmethod.__doc__ == ClassToTestDocs.cmethod.__doc__,
                    k.stmethod.__doc__ == ClassToTestDocs.stmethod.__doc__,
                    k.method.__doc__ == ClassToTestDocs.method.__doc__,
                    k().method.__doc__ == ClassToTestDocs().method.__doc__,
                ]
            )
            assert docs.endswith(template)
            assert to_test
