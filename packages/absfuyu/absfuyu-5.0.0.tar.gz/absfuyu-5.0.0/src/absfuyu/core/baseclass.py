"""
Absfuyu: Core
-------------
Bases for other features

Version: 5.0.0
Date updated: 12/02/2025 (dd/mm/yyyy)
"""

# Module Package
# ---------------------------------------------------------------------------
__all__ = [
    # Color
    "CLITextColor",
    # Mixins
    "ShowAllMethodsMixin",
    "AutoREPRMixin",
    # Class
    "BaseClass",
    # Metaclass
    "PositiveInitArgsMeta",
]


# Color
# ---------------------------------------------------------------------------
class CLITextColor:
    """Color code for text in terminal"""

    WHITE = "\x1b[37m"
    BLACK = "\x1b[30m"
    BLUE = "\x1b[34m"
    GRAY = "\x1b[90m"
    GREEN = "\x1b[32m"
    RED = "\x1b[91m"
    DARK_RED = "\x1b[31m"
    MAGENTA = "\x1b[35m"
    YELLOW = "\x1b[33m"
    RESET = "\x1b[39m"


# Mixins
# ---------------------------------------------------------------------------
class ShowAllMethodsMixin:
    """
    Show all methods of the class and its parent class minus ``object`` class

    *This class is meant to be used with other class*
    """

    @classmethod
    def show_all_methods(
        cls,
        include_classmethod: bool = True,
        classmethod_indicator: str = "<classmethod>",
        include_staticmethod: bool = True,
        staticmethod_indicator: str = "<staticmethod>",
        include_private_method: bool = False,
        print_result: bool = False,
    ) -> dict[str, list[str]]:
        """
        Class method to display all methods of the class and its parent classes,
        including the class in which they are defined in alphabetical order.

        Parameters
        ----------
        include_classmethod : bool, optional
            Whether to include classmethod in the output, by default ``True``

        classmethod_indicator : str, optional
            A string used to mark classmethod in the output. This string is appended
            to the name of each classmethod to visually differentiate it from regular
            instance methods, by default ``"<classmethod>"``

        include_staticmethod : bool, optional
            Whether to include staticmethod in the output, by default ``True``

        staticmethod_indicator : str, optional
            A string used to mark staticmethod in the output. This string is appended
            to the name of each staticmethod to visually differentiate it from regular
            instance methods, by default ``"<staticmethod>"``

        include_private_method : bool, optional
            Whether to include private method in the output, by default ``False``

        print_result : bool, optional
            Beautifully print the output, by default ``False``

        Returns
        -------
        dict[str, list[str]]
            A dictionary where keys are class names and values are lists of method names.
        """
        classes = cls.__mro__[::-1][1:]  # MRO in reverse order
        result = {}
        for base in classes:
            methods = []
            for name, attr in base.__dict__.items():
                # Skip private attribute
                if name.startswith("__"):
                    continue

                # Skip private Callable
                if base.__name__ in name and not include_private_method:
                    continue

                # Function
                if callable(attr):
                    if isinstance(attr, staticmethod):
                        if include_staticmethod:
                            methods.append(f"{name} {staticmethod_indicator}")
                    else:
                        methods.append(name)
                if isinstance(attr, classmethod) and include_classmethod:
                    methods.append(f"{name} {classmethod_indicator}")

            if methods:
                result[base.__name__] = sorted(methods)

        if print_result:
            cls.__print_show_all_result(result)

        return result

    @classmethod
    def show_all_properties(cls, print_result: bool = False) -> dict[str, list[str]]:
        """
        Class method to display all properties of the class and its parent classes,
        including the class in which they are defined in alphabetical order.

        Parameters
        ----------
        print_result : bool, optional
            Beautifully print the output, by default ``False``

        Returns
        -------
        dict[str, list[str]]
            A dictionary where keys are class names and values are lists of property names.
        """
        classes = cls.__mro__[::-1][1:]  # MRO in reverse order
        result = {}
        for base in classes:
            properties = []
            for name, attr in base.__dict__.items():
                # Skip private attribute
                if name.startswith("__"):
                    continue

                if isinstance(attr, property):
                    properties.append(name)

            if properties:
                result[base.__name__] = sorted(properties)

        if print_result:
            cls.__print_show_all_result(result)

        return result

    @staticmethod
    def __print_show_all_result(result: dict[str, list[str]]) -> None:
        """
        Pretty print the result of ``ShowAllMethodsMixin.show_all_methods()``

        Parameters
        ----------
        result : dict[str, list[str]]
            Result of ``ShowAllMethodsMixin.show_all_methods()``
        """
        print_func = print  # Can be extended with function parameter

        # Loop through each class base
        for order, (class_base, methods) in enumerate(result.items(), start=1):
            mlen = len(methods)  # How many methods in that class
            print_func(f"{order:02}. <{class_base}> | len: {mlen:02}")

            # Modify methods list
            max_method_name_len = max([len(x) for x in methods])
            if mlen % 2 == 0:
                p1, p2 = methods[: int(mlen / 2)], methods[int(mlen / 2) :]
            else:
                p1, p2 = methods[: int(mlen / 2) + 1], methods[int(mlen / 2) + 1 :]
                p2.append("")
            new_methods = list(zip(p1, p2))

            # This print 2 methods in 1 line
            for x1, x2 in new_methods:
                if x2 == "":
                    print_func(f"    - {x1.ljust(max_method_name_len)}")
                else:
                    print_func(
                        f"    - {x1.ljust(max_method_name_len)}    - {x2.ljust(max_method_name_len)}"
                    )

            # This print 1 method in one line
            # for name in methods:
            #     print(f"    - {name.ljust(max_method_name_len)}")

            print_func("".ljust(88, "-"))


class AutoREPRMixin:
    """
    Generate ``repr()`` output as ``<class(param1=any, param2=any, ...)>``

    *This class is meant to be used with other class*


    Example:
    --------
    >>> class Test(AutoREPRMixin):
    ...     def __init__(self, param):
    ...         self.param = param
    >>> print(repr(Test(1)))
    Test(param=1)
    """

    def __repr__(self) -> str:
        """
        Generate a string representation of the instance's attributes.

        This function retrieves attributes from either the ``__dict__`` or
        ``__slots__`` of the instance, excluding private attributes (those
        starting with an underscore). The attributes are returned as a
        formatted string, with each attribute represented as ``"key=value"``.

        Convert ``self.__dict__`` from ``{"a": "b"}`` to ``a=repr(b)``
        or ``self.__slots__`` from ``("a",)`` to ``a=repr(self.a)``
        (excluding private attributes)
        """
        # Default output
        out = []
        sep = ", "  # Separator

        # Get attributes
        cls_dict = getattr(self, "__dict__", None)
        cls_slots = getattr(self, "__slots__", None)

        # Check if __dict__ exist and len(__dict__) > 0
        if cls_dict is not None and len(cls_dict) > 0:
            out = [
                f"{k}={repr(v)}"
                for k, v in self.__dict__.items()
                if not k.startswith("_")
            ]

        # Check if __slots__ exist and len(__slots__) > 0
        elif cls_slots is not None and len(cls_slots) > 0:
            out = [
                f"{x}={repr(getattr(self, x))}"
                for x in self.__slots__  # type: ignore
                if not x.startswith("_")
            ]

        # Return out
        return f"{self.__class__.__name__}({sep.join(out)})"


# Class
# ---------------------------------------------------------------------------
class BaseClass(ShowAllMethodsMixin, AutoREPRMixin):
    """Base class"""

    def __str__(self) -> str:
        return repr(self)

    def __format__(self, format_spec: str) -> str:
        """
        Formats the object according to the specified format.
        If no format_spec is provided, returns the object's string representation.
        (Currently a dummy function)

        Usage
        -----
        >>> print(f"{<object>:<format_spec>}")
        >>> print(<object>.__format__(<format_spec>))
        >>> print(format(<object>, <format_spec>))
        """

        return self.__str__()


# Metaclass
# ---------------------------------------------------------------------------
class PositiveInitArgsMeta(type):
    """Make sure that every args in a class __init__ is positive"""

    def __call__(cls, *args, **kwargs):
        # Check if all positional and keyword arguments are positive
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError(f"Argument {arg} must be positive")
        for key, value in kwargs.items():
            if isinstance(value, (int, float)) and value < 0:
                raise ValueError(f"Argument {key}={value} must be positive")

        # Call the original __init__ method
        return super().__call__(*args, **kwargs)
