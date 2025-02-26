import re
import pytest
from milgeo.utils.iter_utils import batched

@pytest.mark.parametrize("iterable, n, strict, expected", [
    ("ABCDEFG", 3, False, [("A", "B", "C"), ("D", "E", "F"), ("G",)]),
    ("ABCDEFG", 3, True, [("A", "B", "C"), ("D", "E", "F")]),
    (range(10), 4, False, [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9)]),
    (range(10), 4, True, [(0, 1, 2, 3), (4, 5, 6, 7)]),
    ("", 2, False, []),
    ("", 2, True, []),
])
def test_batched(iterable, n, strict, expected):
    if strict and len(iterable) % n != 0:
        with pytest.raises(ValueError, match=re.escape("batched(): incomplete batch")):
            list(batched(iterable, n, strict=strict))
    else:
        assert list(batched(iterable, n, strict=strict)) == expected

@pytest.mark.parametrize("iterable, n", [
    ("ABCDEFG", 0),
    ("ABCDEFG", -1),
])
def test_batched_invalid_n(iterable, n):
    with pytest.raises(ValueError, match="n must be at least one"):
        list(batched(iterable, n))
