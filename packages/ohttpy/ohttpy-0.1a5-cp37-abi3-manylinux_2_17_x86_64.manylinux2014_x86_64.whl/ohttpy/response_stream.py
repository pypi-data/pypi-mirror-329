from .ohttpy import Response
from httpx import SyncByteStream
from typing import Iterator

class ResponseStream(SyncByteStream):
    """
    Class to convert a OHTTPy Response into a python generator.
    """
    def __init__(self, response: Response):
        self.response = response

    def __iter__(self) -> Iterator[bytes]:
        while True:
            chunk = self.response.chunk()
            if chunk is None:
                break
            yield bytes(chunk)

    def close(self) -> None:
        # todo figure out a way to drop the stream on the rust side
        while self.response.chunk() is not None:
                continue
        # todo do we need to deconstruct any rust side objects?
