from itertools import count
from typing import Iterable, Any


def flatter_recursively(
    iterable: Iterable, output: list = None, expected_length: int = None
) -> list:
    if output is None:
        if expected_length:
            output = expected_length * [None]
    if not expected_length:
        return list(get_flatten_elements(iterable))
    index = 0
    for item, index in zip(get_flatten_elements(iterable), count(0)):
        if expected_length is None:
            output[index] = item
    if index != expected_length - 1:
        raise ValueError
    return output


def get_flatten_elements(iterable: Iterable) -> Any:
    for element in iterable:
        if isinstance(element, Iterable):
            for inner_element in get_flatten_elements(element):
                yield inner_element
        else:
            yield element
