from types import TracebackType
from typing import Any
from typing import Callable
from typing import Iterable

HeaderList = list[tuple[str, str]]
HeadersList = HeaderList
WSGIEnviron = dict[str, Any]
StartResponse = Callable[[str, HeaderList], None]
WSGICallable = Callable[
    [
        WSGIEnviron,
        StartResponse,
    ],
    Iterable[bytes]
]
ExcInfoTuple = tuple[type, BaseException, TracebackType]
