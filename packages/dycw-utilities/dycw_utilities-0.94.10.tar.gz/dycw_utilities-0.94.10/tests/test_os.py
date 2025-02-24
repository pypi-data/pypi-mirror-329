from __future__ import annotations

from os import getenv
from typing import Literal

from hypothesis import given
from hypothesis.strategies import booleans, integers, sampled_from
from pytest import raises

from utilities.hypothesis import text_ascii
from utilities.os import (
    CPU_COUNT,
    GetCPUUseError,
    get_cpu_count,
    get_cpu_use,
    get_env_var,
    temp_environ,
)
from utilities.pytest import skipif_windows

text = text_ascii(min_size=1, max_size=10)


def _prefix(text: str, /) -> str:
    return f"_TEST_OS_{text}"


class TestGetCPUCount:
    def test_function(self) -> None:
        assert isinstance(get_cpu_count(), int)

    def test_constant(self) -> None:
        assert isinstance(CPU_COUNT, int)


class TestGetCPUUse:
    @given(n=integers(min_value=1))
    def test_int(self, *, n: int) -> None:
        result = get_cpu_use(n=n)
        assert result == n

    def test_all(self) -> None:
        result = get_cpu_use(n="all")
        assert isinstance(result, int)
        assert result >= 1

    @given(n=integers(max_value=0))
    def test_error(self, *, n: int) -> None:
        with raises(GetCPUUseError, match=r"Invalid number of CPUs to use: -?\d+"):
            _ = get_cpu_use(n=n)


class TestGetEnvVar:
    @given(key=text.map(_prefix), value=text)
    @skipif_windows
    def test_case_sensitive(self, *, key: str, value: str) -> None:
        assert getenv(key) is None
        with temp_environ({key: value}):
            assert get_env_var(key) == value

    @given(key=text.map(_prefix), value=text, case=sampled_from(["upper", "lower"]))
    def test_case_insensitive(
        self, *, key: str, value: str, case: Literal["lower", "upper"]
    ) -> None:
        match case:
            case "lower":
                key_use = key.lower()
            case "upper":
                key_use = key.upper()
        with temp_environ({key: value}):
            assert get_env_var(key_use, case_sensitive=False) == value

    @given(key=text.map(_prefix), value=text, case_sensitive=booleans())
    def test_error_case_sensitive_empty(
        self, *, key: str, value: str, case_sensitive: bool
    ) -> None:
        with temp_environ({key: value}):
            assert get_env_var(_prefix(key), case_sensitive=case_sensitive) is None


class TestTempEnviron:
    @given(key=text.map(_prefix), value=text)
    def test_set(self, *, key: str, value: str) -> None:
        assert getenv(key) is None
        with temp_environ({key: value}):
            assert getenv(key) == value
        assert getenv(key) is None

    @given(key=text.map(_prefix), prev=text, new=text)
    def test_override(self, *, key: str, prev: str, new: str) -> None:
        with temp_environ({key: prev}):
            assert getenv(key) == prev
            with temp_environ({key: new}):
                assert getenv(key) == new
            assert getenv(key) == prev

    @given(key=text.map(_prefix), value=text)
    def test_unset(self, *, key: str, value: str) -> None:
        with temp_environ({key: value}):
            assert getenv(key) == value
            with temp_environ({key: None}):
                assert getenv(key) is None
            assert getenv(key) == value
