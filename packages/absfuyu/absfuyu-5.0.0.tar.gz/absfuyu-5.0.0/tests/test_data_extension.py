"""
Test: Data extension

Version: 5.0.0
Date updated: 14/02/2025 (dd/mm/yyyy)
"""

import pytest

from absfuyu.dxt import (
    DictAnalyzeResult,
    DictExt,
    IntExt,
    ListExt,
    Text,
    TextAnalyzeDictFormat,
)


# MARK: fixture
@pytest.fixture
def dict_example():
    return DictExt({"Line 1": 99, "Line 2": 50})


@pytest.fixture
def dict_example_2():
    return DictExt({"Line 1": 99, "Line 2": "test"})


@pytest.fixture
def num_a():
    return IntExt(5)


@pytest.fixture
def num_b():
    return IntExt(10)


@pytest.fixture
def num_prime():
    return IntExt(79)


@pytest.fixture
def list_example():
    return ListExt([3, 8, 5, "Test", "String", "ABC", [1, 2, 3], [0, 8, 6]])


@pytest.fixture
def list_example_2():
    return ListExt(["Test", "String", "ABC", "Tension", "Tent", "Strong"])


@pytest.fixture
def example_long_text():
    return Text(
        "This is an extremely long text that even surpass my expectation and the rest of this text probably contains some useless stuff"
    )


# MARK: DictExt
@pytest.mark.abs_dxt
class TestDictExt:
    """absfuyu.dxt.DictExt"""

    # analyze
    def test_analyze(self, dict_example: DictExt) -> None:
        # assert example.analyze() == {'max_value': 99, 'min_value': 50, 'max': [('Line 1', 99)], 'min': [('Line 2', 50)]}
        assert dict_example.analyze() == DictAnalyzeResult(
            99, 50, [("Line 1", 99)], [("Line 2", 50)]
        )

    def test_analyze_error(self, dict_example_2: DictExt) -> None:
        """When values are not int or float"""
        with pytest.raises(ValueError) as excinfo:
            dict_example_2.analyze()
        assert str(excinfo.value)

    # swap
    def test_swap(self, dict_example: DictExt) -> None:
        assert dict_example.swap_items() == {99: "Line 1", 50: "Line 2"}

    # apply
    def test_apply(self, dict_example: DictExt) -> None:
        """Values"""
        assert dict_example.apply(str) == {"Line 1": "99", "Line 2": "50"}

    def test_apply_2(self) -> None:
        """Keys"""
        assert DictExt({1: 1}).apply(str, apply_to_value=False) == {"1": 1}

    # aggregate
    def test_aggregate(self, dict_example: DictExt) -> None:
        agg = {"Line 1": 1, "Line 3": 1}
        new_dict = dict_example.aggregate(agg)
        assert new_dict == {"Line 1": 100, "Line 2": 50, "Line 3": 1}

    def test_aggregate_2(self, dict_example: DictExt) -> None:
        """Empty dict"""
        new_dict = DictExt().aggregate(dict_example)
        assert new_dict == dict_example

    def test_aggregate_3(self, dict_example: DictExt) -> None:
        """Different type of data"""
        agg = {"Line 1": "1", "Line 3": 1}
        new_dict = dict_example.aggregate(agg)
        assert new_dict == {"Line 1": [99, "1"], "Line 2": 50, "Line 3": 1}


# MARK: IntExt
@pytest.mark.abs_dxt
class TestIntExt:
    """absfuyu.dxt.IntExt"""

    # operation
    def test_operation(self, num_a: IntExt, num_b: IntExt) -> None:
        assert num_a + num_b == 15  # add
        assert num_a - num_b == -5  # subtract
        assert num_a * num_b == 50  # multiply
        assert num_a / num_b == 0.5  # divide
        assert (num_a > num_b) is False  # comparison

    # binary
    @pytest.mark.parametrize(
        ["number", "output"], [(10, "1010"), (10, format(10, "b"))]
    )
    def test_to_binary(self, number: int, output: str) -> None:
        instance: IntExt = IntExt(number)
        assert instance.to_binary() == output

    # reverse
    @pytest.mark.parametrize(["number", "output"], [(10, 1), (5, 5), (79, 97)])
    def test_to_reverse(self, number: int, output: int) -> None:
        instance: IntExt = IntExt(number)
        assert instance.reverse() == output

    # prime
    @pytest.mark.parametrize(["number", "output"], [(79, True), (33, False)])
    def test_is_prime(self, number: int, output: bool) -> None:
        instance: IntExt = IntExt(number)
        assert instance.is_prime() is output

    @pytest.mark.parametrize(["number", "output"], [(79, True), (53, False)])
    def test_is_twisted_prime(self, number: int, output: bool) -> None:
        instance: IntExt = IntExt(number)
        assert instance.is_twisted_prime() is output

    @pytest.mark.parametrize(["number", "output"], [(797, True), (79, False)])
    def test_is_palindromic_prime(self, number: int, output: bool) -> None:
        instance: IntExt = IntExt(number)
        assert instance.is_palindromic_prime() is output

    # perfect
    @pytest.mark.parametrize(["number", "output"], [(28, True), (22, False)])
    def test_is_perfect(self, number: int, output: bool) -> None:
        instance: IntExt = IntExt(number)
        assert instance.is_perfect() is output

    # narcissistic
    @pytest.mark.parametrize(["number", "output"], [(371, True), (46, False)])
    def test_is_narcissistic(self, number: int, output: bool) -> None:
        instance: IntExt = IntExt(number)
        assert instance.is_narcissistic() is output

    # palindromic
    @pytest.mark.parametrize(["number", "output"], [(12321, True), (1231, False)])
    def test_is_palindromic(self, number: int, output: bool) -> None:
        instance: IntExt = IntExt(number)
        assert instance.is_palindromic() is output

    # degree
    def test_convert_degree(self, num_a: IntExt) -> None:
        assert num_a.to_celcius_degree() == -15.0
        assert num_a.to_fahrenheit_degree() == 41.0

    # even
    @pytest.mark.parametrize(["number", "output"], [(2, True), (3, False)])
    def test_is_even(self, number: int, output: bool) -> None:
        instance: IntExt = IntExt(number)
        assert instance.is_even() is output

    # lcm
    def test_lcm(self, num_a: IntExt) -> None:
        assert num_a.lcm(6) == 30

    # gcd
    def test_gcd(self, num_a: IntExt) -> None:
        assert num_a.gcd(25) == 5

    # add_to_one_digit
    def test_add_to_one_digit(self, num_prime: IntExt) -> None:
        assert num_prime.add_to_one_digit() == 7

    @pytest.mark.parametrize(["number", "output"], [(1091, 11), (994, 22)])
    def test_add_to_one_digit_2(self, number: int, output: int) -> None:
        instance = IntExt(number)
        assert instance.add_to_one_digit(master_number=True) == output

    # analyze
    def test_analyze(self) -> None:
        assert IntExt(51564).analyze()

    # prime factor
    def test_prime_factor(self) -> None:
        assert IntExt(884652).prime_factor(short_form=False) == [2, 2, 3, 73721]

    # divisible_list
    def test_divisible_list(self) -> None:
        assert IntExt(884652).divisible_list() == [
            1,
            2,
            3,
            4,
            6,
            12,
            73721,
            147442,
            221163,
            294884,
            442326,
            884652,
        ]


# MARK: ListExt
@pytest.mark.abs_dxt
class TestListExt:
    """absfuyu.dxt.ListExt"""

    # stringify
    def test_stringify(self, list_example: ListExt) -> None:
        assert all([isinstance(x, str) for x in list_example.stringify()]) is True

    # sorts
    def test_sorts(self, list_example: ListExt) -> None:
        assert list_example.sorts() == [
            3,
            5,
            8,
            "ABC",
            "String",
            "Test",
            [0, 8, 6],
            [1, 2, 3],
        ]

    # freq
    def test_freq(self, list_example_2: ListExt) -> None:
        assert list_example_2.freq(sort=True) == {
            "ABC": 1,
            "String": 1,
            "Strong": 1,
            "Tension": 1,
            "Tent": 1,
            "Test": 1,
        }

    def test_freq_2(self, list_example_2: ListExt) -> None:
        assert list_example_2.freq(sort=True, num_of_first_char=2) == {
            "AB": 1,
            "St": 2,
            "Te": 3,
        }

    def test_freq_3(self, list_example_2: ListExt) -> None:
        assert list_example_2.freq(
            sort=True, num_of_first_char=2, appear_increment=True
        ) == [1, 3, 6]

    # slice_points
    def test_slice_points(self, list_example_2: ListExt) -> None:
        assert list_example_2.slice_points([1, 3]) == [
            ["Test"],
            ["String", "ABC"],
            ["Tension", "Tent", "Strong"],
        ]

    # pick_one
    def test_pick_one(self, list_example_2: ListExt) -> None:
        assert len([list_example_2.pick_one()]) == 1

    def test_pick_one_error(self) -> None:
        """Empty list"""
        with pytest.raises(IndexError) as excinfo:
            ListExt([]).pick_one()
            assert str(excinfo.value)

    # len_items
    def test_len_items(self, list_example_2: ListExt) -> None:
        assert list_example_2.len_items() == [4, 6, 3, 7, 4, 6]

    # mean_len
    def test_mean_len(self, list_example_2: ListExt) -> None:
        assert list_example_2.mean_len() == 5.0

    # apply
    def test_apply(self, list_example: ListExt) -> None:
        assert list_example.apply(str) == list_example.stringify()

    # unique
    def test_unique(self) -> None:
        assert ListExt([1, 1, 1, 1]).unique() == [1]

    # head
    def test_head(self, list_example: ListExt) -> None:
        assert list_example.head(3) == [3, 8, 5]

    def test_head_2(self, list_example: ListExt) -> None:
        """Max head len"""
        assert list_example.head(100) == list(list_example)

    def test_head_3(self) -> None:
        """Empty list"""
        assert ListExt([]).head(9) == []

    # tail
    def test_tail(self, list_example_2: ListExt) -> None:
        assert list_example_2.tail(2) == ["Tent", "Strong"]

    def test_tail_2(self, list_example_2: ListExt) -> None:
        assert list_example_2.tail(100) == list(list_example_2)

    def test_tail_3(self) -> None:
        """Empty list"""
        assert ListExt([]).tail(9) == []

    # get_random
    def test_get_random(self, list_example_2: ListExt) -> None:
        test = list_example_2.get_random(20)
        assert len(test) == 20

    # flatten
    def test_flatten(self, list_example: ListExt) -> None:
        test = list_example.flatten()
        assert test


# MARK: Text
@pytest.mark.abs_dxt
class TestText:
    """absfuyu.dxt.Text"""

    # analyze
    @pytest.mark.parametrize(
        ["value", "output"],
        [
            (
                "Lmao",
                {
                    "digit": 0,
                    "uppercase": 1,
                    "lowercase": 3,
                    "other": 0,
                },
            ),
            ("Lmao$$TEST.", {"digit": 0, "uppercase": 5, "lowercase": 3, "other": 3}),
        ],
    )
    def test_analyze(self, value: str, output: TextAnalyzeDictFormat) -> None:
        assert Text(value).analyze() == output

    # hex
    def test_to_hex(self) -> None:
        assert Text("Hello World").to_hex(raw=True) == "48656c6c6f20576f726c64"
        assert (
            Text("Hello World").to_hex()
            == "\\x48\\x65\\x6c\\x6c\\x6f\\x20\\x57\\x6f\\x72\\x6c\\x64"
        )

    # pangram
    @pytest.mark.parametrize(
        ["value", "output"],
        [
            ("abcdeFghijklmnopqrstuvwxyz", True),
            ("abcdefghijklmnOpqrstuvwxy", False),
            ("abcdeFghijklmnopqrstuvwxyzsdsd", True),
            ("abcdeFghijklmnopqrs tuvwxyzsdsd0", True),
        ],
    )
    def test_is_pangram(self, value: str, output: bool) -> None:
        assert Text(value).is_pangram() is output

    def test_is_pangram_custom(self) -> None:
        custom_alphabet = {"a", "b", "c"}
        assert Text("abc").is_pangram(custom_alphabet) is True
        assert Text("ab").is_pangram(custom_alphabet) is False
        assert Text("abcd").is_pangram(custom_alphabet) is True

    # palindrome
    @pytest.mark.parametrize(
        ["value", "output"], [("madam", True), ("racecar", True), ("bomb", False)]
    )
    def test_is_palindrome(self, value: str, output: bool) -> None:
        assert Text(value).is_palindrome() is output

    # reverse
    def test_reverse(self) -> None:
        assert Text("abc").reverse() == "cba"

    # random capslock
    @pytest.mark.parametrize("value", ["random", "capslock"])
    def test_random_capslock(self, value: str) -> None:
        test_0_percent: list[Text] = [
            Text(value).random_capslock(0) for _ in range(1000)
        ]
        test_50_percent: list[Text] = [
            Text(value).random_capslock(50) for _ in range(1000)
        ]
        test_100_percent: list[Text] = [
            Text(value).random_capslock(100) for _ in range(1000)
        ]
        assert len(list(set(test_0_percent))) == 1
        assert len(list(set(test_100_percent))) == 1
        assert Text(value).random_capslock(0) == value.lower()
        assert Text(value).random_capslock(100) == value.upper()

        try:
            assert len(list(set(test_50_percent))) != 1
            assert (
                Text(value).random_capslock(50) != value.lower()
                and Text(value).random_capslock(50) != value.upper()
            )
        except Exception as e:
            assert str(e)

    # divide
    def test_divide(self, example_long_text: Text) -> None:
        assert example_long_text.divide().__len__() == 3
        assert example_long_text.divide(string_split_size=10).__len__() == 13

    def test_divide_with_variable(self, example_long_text: Text) -> None:
        assert example_long_text.divide_with_variable(
            split_size=60, custom_var_name="abc"
        ) == [
            "abc1='This is an extremely long text that even surpass my expectat'",
            "abc2='ion and the rest of this text probably contains some useless'",
            "abc3=' stuff'",
            "abc=abc1+abc2+abc3",
            "abc",
        ]

    def test_divide_with_variable_2(self, example_long_text: Text) -> None:
        """Check for list len"""
        assert (
            example_long_text.divide_with_variable(
                split_size=60, custom_var_name="abc"
            ).__len__()
            == 5
        )

    # reverse capslock
    @pytest.mark.parametrize(
        ["value", "output"], [("Foo", "fOO"), ("Foo BAr", "fOO baR")]
    )
    def test_reverse_capslock(self, value: str, output: str) -> None:
        assert Text(value).reverse_capslock() == output

    # to list
    def test_to_list(self) -> None:
        assert isinstance(Text("test").to_list(), list)
        # assert isinstance(Text("test").to_listext(), ListExt)

    # count pattern
    @pytest.mark.parametrize("value", ["Test sentence"])
    @pytest.mark.parametrize(
        ["pattern", "output"],
        [("ten", 1), ("t", 2), ("a", 0)],
    )
    def test_count_pattern(self, value: str, pattern: str, output: int) -> None:
        assert Text(value).count_pattern(pattern) == output

    def test_count_pattern_2(self) -> None:
        assert Text("Test sentence").count_pattern("t", ignore_capslock=True) == 3

    def test_count_pattern_error(self) -> None:
        with pytest.raises(ValueError) as excinfo:
            Text("Test").count_pattern("tenss")
        assert str(excinfo.value)

    # hapax
    def test_hapax(self) -> None:
        assert Text("A a. a, b c c= C| d d").hapax() == [
            "a",
            "a.",
            "a,",
            "b",
            "c",
            "c=",
            "c|",
        ]

    def test_hapax_2(self) -> None:
        assert Text("A a. a, b c c= C| d d").hapax(strict=True) == ["b"]

    # shorten
    def test_shorten(self, example_long_text: Text) -> None:
        example_long_text.shorten()

    def test_shorten_negative_parameter(self, example_long_text: Text) -> None:
        example_long_text.shorten(-99)
