import requests
from typing import Any
from io import BytesIO
import datetime
from .ohttpy import Client
from ohttpy.response_stream import ResponseStream

class Session(requests.Session):
    def __init__(self) -> None:
        super().__init__()
        self.client = Client()

    def to_bytes(self, data: Any) -> bytes:
        if isinstance(data, bytes):
            return data
        elif isinstance(data, str):
            return data.encode('utf-8')
        elif hasattr(data, 'read'):  # For file-like objects
            return data.read()
        elif data is None:
            return b""
        else:
            raise ValueError("Unsupported data type for conversion to bytes")


    def send(self, request: requests.PreparedRequest, **kwargs: Any) -> requests.Response:
        """
        Encrypt the request body, send the request, and decrypt the response.
        Args:
            request (PreparedRequest): The HTTP request to send.
            **kwargs (Any): Additional arguments for the send method.
        Returns:
            Response: The HTTP response.
        """
        # call binding to py OHTTP client
        response = self.client.send_request(
            method=request.method, url=request.url,
            headers=dict(request.headers), body=self.to_bytes(request.body))

        # translate response into requests.response compatible format
        status_code = response.status_code()
        headers = response.headers()
        body = bytes().join([x for x in ResponseStream(response)])

        # construct a compatible requests.Response object
        ret_response = requests.Response()
        ret_response.status_code = status_code
        ret_response.reason = requests.status_codes._codes[status_code][0].replace("_", " ").title()
        ret_response.headers = requests.structures.CaseInsensitiveDict(headers)

        # below fields are informational...
        ret_response.request = request
        ret_response.url = request.url

        # TODO figure out if chunk stream can be sent back as BytesIO stream
        # If streaming is requested, return a BytesIO stream (mimicking a real stream)
        if kwargs.get("stream", False):
            # Simulate a file-like streaming object for compatibility
            ret_response.raw = BytesIO(body)
        else:
            # Fully load content into memory (normal behavior)
            ret_response._content = body
            # handle response_body type error
            ret_response.raw = BytesIO(body)  # Still provide raw access for consistency

        # Set elapsed time (mocked, since we're not timing)
        ret_response.elapsed = datetime.timedelta(seconds=0)

        return ret_response