"""
Absfuyu: Data Extension
-----------------------
list extension

Version: 5.0.0
Date updated: 11/02/2025 (dd/mm/yyyy)
"""

# Module Package
# ---------------------------------------------------------------------------
__all__ = ["ListExt"]


# Library
# ---------------------------------------------------------------------------
import operator
import random
from collections import Counter
from collections.abc import Callable
from itertools import accumulate, chain, groupby
from typing import Any, Self

from absfuyu.core import ShowAllMethodsMixin, deprecated
from absfuyu.util import set_min, set_min_max


# Class
# ---------------------------------------------------------------------------
class ListExt(ShowAllMethodsMixin, list):
    """
    ``list`` extension
    """

    def stringify(self) -> Self:
        """
        Convert all item in ``list`` into string

        Returns
        -------
        ListExt
            A list with all items with type <str`>


        Example:
        --------
        >>> test = ListExt([1, 1, 1, 2, 2, 3])
        >>> test.stringify()
        ['1', '1', '1', '2', '2', '3']
        """
        return self.__class__(map(str, self))

    def head(self, number_of_items: int = 5) -> list:
        """
        Show first ``number_of_items`` items in ``ListExt``

        Parameters
        ----------
        number_of_items : int
            | Number of items to shows at once
            | (Default: ``5``)

        Returns
        -------
        list
            Filtered list
        """
        number_of_items = int(
            set_min_max(number_of_items, min_value=0, max_value=len(self))
        )
        return self[:number_of_items]

    def tail(self, number_of_items: int = 5) -> list:
        """
        Show last ``number_of_items`` items in ``ListExt``

        Parameters
        ----------
        number_of_items : int
            | Number of items to shows at once
            | (Default: ``5``)

        Returns
        -------
        list
            Filtered list
        """
        number_of_items = int(
            set_min_max(number_of_items, min_value=0, max_value=len(self))
        )
        return self[::-1][:number_of_items][::-1]

    def sorts(self, reverse: bool = False) -> Self:
        """
        Sort all items (with different type) in ``list``

        Parameters
        ----------
        reverse : bool
            | if ``True`` then sort in descending order
            | if ``False`` then sort in ascending order
            | (Default: ``False``)

        Returns
        -------
        ListExt
            A sorted list


        Example:
        --------
        >>> test = ListExt([9, "abc", 3.5, "aaa", 1, 1.4])
        >>> test.sorts()
        [1, 9, 'aaa', 'abc', 1.4, 3.5]
        """
        lst = self.copy()
        type_weights: dict = {}
        for x in lst:
            if type(x) not in type_weights:
                type_weights[type(x)] = len(type_weights)
        # logger.debug(f"Type weight: {type_weights}")

        output = sorted(
            lst, key=lambda x: (type_weights[type(x)], str(x)), reverse=reverse
        )

        # logger.debug(output)
        return self.__class__(output)

    def freq(
        self,
        sort: bool = False,
        num_of_first_char: int | None = None,
        appear_increment: bool = False,
    ) -> dict | list[int]:
        """
        Find frequency of each item in list

        Parameters
        ----------
        sort : bool
            | if ``True``: Sorts the output in ascending order
            | if ``False``: No sort

        num_of_first_char : int | None
            | Number of first character taken into account to sort
            | (Default: ``None``)
            | (num_of_first_char = ``1``: first character in each item)

        appear_increment : bool
            | return incremental index list of each item when sort
            | (Default: ``False``)

        Returns
        -------
        dict
            A dict that show frequency

        list[int]
            Incremental index list


        Example:
        --------
        >>> test = ListExt([1, 1, 2, 3, 5, 5])
        >>> test.freq()
        {1: 2, 2: 1, 3: 1, 5: 2}

        >>> test = ListExt([1, 1, 2, 3, 3, 4, 5, 6])
        >>> test.freq(appear_increment=True)
        [2, 3, 5, 6, 7, 8]
        """

        if sort:
            data = self.sorts().copy()
        else:
            data = self.copy()

        if num_of_first_char is None:
            temp = Counter(data)
        else:
            max_char: int = min([len(str(x)) for x in data])
            # logger.debug(f"Max character: {max_char}")
            if num_of_first_char not in range(1, max_char):
                # logger.debug(f"Not in {range(1, max_char)}. Using default value...")
                temp = Counter(data)
            else:
                # logger.debug(f"Freq of first {num_of_first_char} char")
                temp = Counter([str(x)[:num_of_first_char] for x in data])

        try:
            times_appear = dict(sorted(temp.items()))
        except Exception:
            times_appear = dict(self.__class__(temp.items()).sorts())
        # logger.debug(times_appear)

        if appear_increment:
            times_appear_increment: list[int] = list(
                accumulate(times_appear.values(), operator.add)
            )
            # logger.debug(times_appear_increment)
            return times_appear_increment  # incremental index list
        else:
            return times_appear  # character frequency

    def slice_points(self, points: list[int]) -> list[list]:
        """
        Splits a list into sublists based on specified split points (indices).

        This method divides the original list into multiple sublists. The ``points``
        argument provides the indices at which the list should be split.  The resulting
        list of lists contains the sublists created by these splits. The original
        list is not modified.

        Parameters
        ----------
        points : list
            A list of integer indices representing the points at which to split
            the list. These indices are *exclusive* of the starting sublist
            but *inclusive* of the ending sublist.

        Returns
        -------
        list[list]
            A list of lists, where each inner list is a slice of the original list
            defined by the provided split points.


        Example:
        --------
        >>> test = ListExt([1, 1, 2, 3, 3, 4, 5, 6])
        >>> test.slice_points([2, 5])
        [[1, 1], [2, 3, 3], [4, 5, 6]]
        >>> test.slice_points([0, 1, 2, 3, 4, 5, 6, 7, 8])
        [[], [1], [1], [2], [3], [3], [4], [5], [6]]
        >>> test.slice_points([])
        [[1, 1, 2, 3, 3, 4, 5, 6]]
        """
        points.append(len(self))
        data = self.copy()
        # return [data[points[i]:points[i+1]] for i in range(len(points)-1)]
        return [data[i1:i2] for i1, i2 in zip([0] + points[:-1], points)]

    def pick_one(self) -> Any:
        """
        Pick one random items from ``list``

        Returns
        -------
        Any
            Random value


        Example:
        --------
        >>> test = ListExt(["foo", "bar"])
        >>> test.pick_one()
        'bar'
        """
        if len(self) != 0:
            out = random.choice(self)
            # logger.debug(out)
            return out
        else:
            # logger.debug("List empty!")
            raise IndexError("List empty!")

    def get_random(self, number_of_items: int = 5) -> list:
        """
        Get ``number_of_items`` random items in ``ListExt``

        Parameters
        ----------
        number_of_items : int
            | Number random of items
            | (Default: ``5``)

        Returns
        -------
        list
            Filtered list
        """
        return [self.pick_one() for _ in range(number_of_items)]

    def len_items(self) -> Self:
        """
        ``len()`` for every item in ``list[str]``

        Returns
        -------
        ListExt
            List of ``len()``'ed value


        Example:
        --------
        >>> test = ListExt(["foo", "bar", "pizza"])
        >>> test.len_items()
        [3, 3, 5]
        """
        out = self.__class__([len(str(x)) for x in self])
        # out = ListExt(map(lambda x: len(str(x)), self))
        # logger.debug(out)
        return out

    def mean_len(self) -> float:
        """
        Average length of every item

        Returns
        -------
        float
            Average length


        Example:
        --------
        >>> test = ListExt(["foo", "bar", "pizza"])
        >>> test.mean_len()
        3.6666666666666665
        """
        out = sum(self.len_items()) / len(self)
        # logger.debug(out)
        return out

    def apply(self, func: Callable) -> Self:
        """
        Apply function to each entry

        Parameters
        ----------
        func : Callable
            Callable function

        Returns
        -------
        ListExt
            ListExt


        Example:
        --------
        >>> test = ListExt([1, 2, 3])
        >>> test.apply(str)
        ['1', '2', '3']
        """
        # return __class__(func(x) for x in self)
        return self.__class__(map(func, self))

    def unique(self) -> Self:
        """
        Remove duplicates

        Returns
        -------
        ListExt
            Duplicates removed list


        Example:
        --------
        >>> test = ListExt([1, 1, 1, 2, 2, 3])
        >>> test.unique()
        [1, 2, 3]
        """
        return self.__class__(set(self))

    def group_by_unique(self) -> Self:
        """
        Group duplicated elements into list

        Returns
        -------
        ListExt
            Grouped value


        Example:
        --------
        >>> test = ListExt([1, 2, 3, 1, 3, 3, 2])
        >>> test.group_by_unique()
        [[1, 1], [2, 2], [3, 3, 3]]
        """
        # Old
        # out = self.sorts().slice_points(self.freq(appear_increment=True))
        # return __class__(out[:-1])

        # New
        temp = groupby(self.sorts())
        return self.__class__([list(g) for _, g in temp])

    def group_by_pair_value(self, max_loop: int = 3) -> list[list]:
        """
        Assume each ``list`` in ``list`` is a pair value,
        returns a ``list`` contain all paired value

        Parameters
        ----------
        max_loop : int
            Times to run functions (minimum: ``3``)

        Returns
        -------
        list[list]
            Grouped value


        Example:
        --------
        >>> test = ListExt([[1, 2], [2, 3], [4, 3], [5, 6]])
        >>> test.group_by_pair_value()
        [[1, 2, 3, 4], [5, 6]]

        >>> test = ListExt([[8, 3], [4, 6], [6, 3], [5, 2], [7, 2]])
        >>> test.group_by_pair_value()
        [[8, 3, 4, 6], [2, 5, 7]]

        >>> test = ListExt([["a", 4], ["b", 4], [5, "c"]])
        >>> test.group_by_pair_value()
        [['a', 4, 'b'], ['c', 5]]
        """

        iter = self.copy()

        # Init loop
        for _ in range(int(set_min(max_loop, min_value=3))):
            temp: dict[Any, list] = {}
            # Make dict{key: all `item` that contains `key`}
            for item in iter:
                for x in item:
                    if temp.get(x, None) is None:
                        temp[x] = [item]
                    else:
                        temp[x].append(item)

            # Flatten dict.values
            for k, v in temp.items():
                temp[k] = list(set(chain(*v)))

            iter = list(temp.values())

        return list(x for x, _ in groupby(iter))

    def flatten(self) -> Self:
        """
        Flatten the list

        Returns
        -------
        ListExt
            Flattened list


        Example:
        --------
        >>> test = ListExt([["test"], ["test", "test"], ["test"]])
        >>> test.flatten()
        ['test', 'test', 'test', 'test']
        """
        try:
            # return self.__class__(sum(self, start=[]))
            return self.__class__(chain(*self))
        except Exception:
            temp = list(map(lambda x: x if isinstance(x, list) else [x], self))
            return self.__class__(chain(*temp))

    def numbering(self, start: int = 0) -> Self:
        """
        Number the item in list
        (``enumerate`` wrapper)

        Parameters
        ----------
        start : int
            Start from which number
            (Default: ``0``)

        Returns
        -------
        ListExt
            Counted list


        Example:
        --------
        >>> test = ListExt([9, 9, 9])
        >>> test.numbering()
        [(0, 9), (1, 9), (2, 9)]
        """
        start = int(set_min(start, min_value=0))
        return self.__class__(enumerate(self, start=start))

    @staticmethod
    @deprecated("5.0.0")
    def _group_by_unique(iterable: list) -> list[list]:
        """
        Static method for ``group_by_unique``
        """
        return list([list(g) for _, g in groupby(iterable)])

    @staticmethod
    @deprecated("5.0.0")
    def _numbering(iterable: list, start: int = 0) -> list[tuple[int, Any]]:
        """
        Static method for ``numbering``
        """
        start = int(set_min(start, min_value=0))
        return list(enumerate(iterable, start=start))
