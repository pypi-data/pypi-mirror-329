"""
Test: Util

Version: 5.0.0
Date updated: 14/02/2025 (dd/mm/yyyy)
"""

import sys
from pathlib import Path

import pytest

from absfuyu.config import CONFIG_PATH
from absfuyu.util import set_max, set_min, set_min_max
from absfuyu.util.api import APIRequest, PingResult, ping_windows
from absfuyu.util.json_method import JsonFile
from absfuyu.util.path import Directory
from absfuyu.util.performance import retry
from absfuyu.util.shorten_number import CommonUnitSuffixesFactory, Decimal


# MARK: util
@pytest.mark.abs_util
class TestUtil:
    """absfuyu.util"""

    @pytest.mark.parametrize(["value", "output"], [(10, 10), (-5, 0)])
    def test_set_min(self, value: int, output: int) -> None:
        assert set_min(value, min_value=0) == output

    @pytest.mark.parametrize(["value", "output"], [(200, 100), (10, 10)])
    def test_set_max(self, value: int, output: int) -> None:
        assert set_max(value, max_value=100) == output

    @pytest.mark.parametrize(["value", "output"], [(50, 50), (-10, 0), (200, 100)])
    def test_set_min_max(self, value: int, output: int) -> None:
        assert set_min_max(value, min_value=0, max_value=100) == output


# MARK: api
@pytest.mark.abs_util
class TestUtilAPI:
    """absfuyu.util.api"""

    @pytest.mark.skip  # temporary skip
    def test_API(self) -> None:
        instance = APIRequest("https://dummyjson.com/quotes")
        try:
            assert isinstance(instance.fetch_data_only().json()["quotes"], list)
        except Exception:
            # No internet
            assert instance

    @pytest.mark.skipif(
        sys.platform not in ["win32", "cygwin"],
        reason="Not applicable on Linux and MacOS",
    )  # windows only
    def test_ping_windows(self) -> None:
        res = ping_windows(["google.com"], 1)
        assert isinstance(res[0], PingResult)


# MARK: json
@pytest.mark.abs_util
class TestUtilJsonMethod:
    """absfuyu.util.json_method"""

    def test_json_load(self) -> None:
        instance = JsonFile(CONFIG_PATH)
        loaded = instance.load_json()
        assert isinstance(loaded, dict)


# MARK: path
@pytest.mark.abs_util
class TestUtilPath:
    """absfuyu.util.path"""

    def test_list_structure(self) -> None:
        instance = Directory(source_path=Path.cwd())
        assert instance.list_structure_pkg()


# MARK: shorten number
@pytest.mark.abs_util
class TestUtilShortenNumber:
    """absfuyu.util.shorten_number"""

    @pytest.mark.parametrize(["value", "output"], [(1000, 1.0), (1000000, 1.0)])
    def test_number(self, value: int | float, output: float) -> None:
        ins = Decimal.number(value)
        assert ins.value == output

    def test_number2(self) -> None:
        fac = CommonUnitSuffixesFactory.NUMBER
        unit = 1
        for i, suffix in enumerate(fac.short_name):
            unit = fac.base**i
            assert Decimal.number(unit).suffix == suffix

    def test_data_size(self) -> None:
        fac = CommonUnitSuffixesFactory.DATA_SIZE
        unit = 1
        for i, suffix in enumerate(fac.short_name):
            unit = fac.base**i
            assert Decimal.data_size(unit).suffix == suffix


# MARK: performance
@pytest.mark.abs_util
class TestUtilPerformance:
    """absfuyu.util.performance"""

    # retry
    def test_retry_invalid_parameters(self):
        with pytest.raises(
            ValueError, match="retries must be >= 1, delay must be >= 0"
        ):

            @retry(retries=0)
            def invalid_function():
                pass

        with pytest.raises(
            ValueError, match="retries must be >= 1, delay must be >= 0"
        ):

            @retry(retries=3, delay=-1)
            def invalid_function():
                pass

    def test_retry_success(self) -> None:
        @retry(retries=3, delay=0.1)
        def success_function():
            return "Success"

        result = success_function()
        assert result == "Success"

    @pytest.mark.xfail
    def test_retry_failure(self) -> None:
        with pytest.raises(Exception, match="Function error") as excinfo:

            @retry(retries=3, delay=0.1)
            def failing_function():
                raise Exception("Function error")

            failing_function()
        assert str(excinfo.value)

    def test_retry_with_valid_retries(self) -> None:
        @retry(retries=2, delay=0.1)
        def intermittent_failure():
            if intermittent_failure.call_count < 1:
                intermittent_failure.call_count += 1
                raise Exception("Temporary failure")
            return "Success"

        intermittent_failure.call_count = 0  # Initialize call count

        result = intermittent_failure()

        assert result == "Success"
