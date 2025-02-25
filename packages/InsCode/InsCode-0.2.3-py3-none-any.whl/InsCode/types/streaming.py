import json
from types import TracebackType
from typing import Generic, TypeVar, Iterator, Self, Type

import requests

from src.InsCode.util import cast_to

_T = TypeVar("_T")


class Stream(Generic[_T]):
    """Provides the core interface to iterate over a synchronous stream response."""

    response: requests.Response

    def __init__(
            self,
            *,
            cls: Type[_T],
            response: requests.Response,
    ) -> None:
        self.response = response
        self._cls = cls
        self._iterator = self.__stream__()

    def __next__(self) -> _T:
        return self._iterator.__next__()

    def __iter__(self) -> Iterator[_T]:
        for item in self._iterator:
            yield item

    def __stream__(self) -> Iterator[_T]:
        response = self.response

        for line in response.iter_lines(decode_unicode=True):
            if line == '':
                continue

            data_str = line
            if 'data:' in line:
                data_str = line[5:]
            if data_str.lower() == '[done]':
                break
            data = json.loads(data_str)
            instance = cast_to(data, self._cls)
            yield instance

    def __enter__(self) -> Self:
        return self

    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        """
        Close the response and release the connection.

        Automatically called if the response body is read to completion.
        """
        self.response.close()
