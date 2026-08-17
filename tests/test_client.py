import httpx
import unittest

from kaa_rest_client import KaaClient


class KaaClientResponseTests(unittest.IsolatedAsyncioTestCase):
    async def test_request_response_preserves_raw_body_and_headers(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                201,
                headers={"ETag": "abc", "Location": "/ecr/configs/1"},
                json={"ok": True},
                request=request,
            )

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            client = KaaClient(base_url="https://example.test", client=http)
            response = await client.request_response("POST", "/resource")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"ok": True})
        self.assertEqual(response.headers["etag"], "abc")
        self.assertEqual(response.headers["location"], "/ecr/configs/1")

    async def test_request_still_decodes_json_body(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"value": 3}, request=request)

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            client = KaaClient(base_url="https://example.test", client=http)
            result = await client.request("GET", "/resource")

        self.assertEqual(result, {"value": 3})


if __name__ == "__main__":
    unittest.main()
