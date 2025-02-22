import abc
import base64
import hashlib
import sys
import traceback
from typing import Any, Callable, Iterable, Type, TypeVar, Union


primitives = (bool, str, int, float, type(None))


def batched(xs: list, batch_size: int) -> list[list]:
    return [
        xs[i:i + batch_size]
        for i in range(0, len(xs), batch_size)
    ]


def scrub_title_key(d: dict):
    """
    Helpful because pydantic schema dumps include an unecessary 'title' attribute;
    """
    d.pop("title", None)
    if d.get("type") == "object":
        assert "properties" in d
        for prop in d["properties"].keys():
            scrub_title_key(d["properties"][prop])
    return d


def is_primitive(obj):
    return isinstance(obj, primitives)


def get(obj: Any, *attr_path: Union[str, int]):
    cur = obj
    for key in attr_path:
        if cur is None:
            return None
        if type(cur) == list:
            if type(key) != int:
                return None
            if key >= len(cur):
                return None
            cur = cur[key]
        elif type(cur) == dict:
            if key not in cur:
                return None
            cur = cur[key]
        elif is_primitive(cur):
            # can't index a primitive
            return None
        else:
            if type(key) != str:
                return None
            cur = getattr(cur, key, None)
    return cur


T = TypeVar("T")
S = TypeVar("S")
E = TypeVar("E", bound=Exception)


class TracebackError(Exception, abc.ABC):
    def __init__(self, *args: object, tb: str = ""):
        pass


def try_or_raise(fn: Callable[[], T], exc: Type[TracebackError]) -> T:
    """
    Try 'fn()', raising 'exc' on any exception.
    """
    try:
        return fn()
    except Exception as e:
        exc_info = sys.exc_info()
        tb = "".join(traceback.format_exception(*exc_info))
        raise exc(e, tb=tb)
    return


def try_or(
    fn: Callable[[], T], on_err: Callable[[E], S], errtype: Type[E]
) -> Union[T, S]:
    """
    Try 'fn()', but call 'on_err' if an error of 'errtype' is thrown.
    """
    try:
        return fn()
    except errtype as e:
        return on_err(e)
    return


def map_multithreaded(fn, data: Iterable, max_threads: int) -> list:
    """
    Like builtin 'map', but executes across 'max_threads' threads, and returns a list not an iterator.
    Here, order will be preserved.
    """
    if not data:
        return []
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        return list(executor.map(fn, data))
    return


def concurrently(*fns) -> list:
    """
    Call all provided functions in their own thread, returning the results in a list.
    """

    def call(fn):
        return fn()

    return map_multithreaded(call, fns, len(fns))


def md5_b64_str(contents: str) -> str:
    result = hashlib.md5(contents.encode("utf-8"))
    digest = result.digest()
    return base64.b64encode(digest).decode("utf-8")
