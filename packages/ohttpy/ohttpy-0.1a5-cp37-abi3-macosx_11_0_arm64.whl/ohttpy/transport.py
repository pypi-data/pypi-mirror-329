import httpx
from .ohttpy import Client
from ohttpy.response_stream import ResponseStream


# Custom HTTP Transport that integrates OHTTP
class Transport(httpx.BaseTransport):
    def __init__(self):
        # create binding object to OHTTPy client
        self.client = Client()

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        # call binding to py OHTTPy client
        response = self.client.send_request(
            method=request.method, url=str(request.url),
            headers=dict(request.headers), body=request.content)

        # translate response into httpx compatible format
        status_code = response.status_code()
        headers = response.headers()
        stream = ResponseStream(response)

        # construct httpx response
        httpx_response = httpx.Response(
            status_code=status_code, headers=headers,
            request=request, stream=stream)

        return httpx_response
