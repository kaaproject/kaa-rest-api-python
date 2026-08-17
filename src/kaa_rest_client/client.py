from __future__ import annotations

import contextvars
from typing import Any

import httpx

from .exceptions import KaaApiError, KaaAuthError, KaaNotFoundError

request_api_key: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_api_key", default=None
)
request_bearer_token: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_bearer_token", default=None
)
request_tenant_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_tenant_id", default=None
)
request_base_url: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_base_url", default=None
)


class KaaClient:
    def __init__(
        self,
        base_url: str = "https://next.kaaiot.com",
        api_key: str | None = None,
        bearer_token: str | None = None,
        client: httpx.AsyncClient | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._bearer_token = bearer_token
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            limits=httpx.Limits(
                max_connections=20,
                max_keepalive_connections=10,
            ),
        )

    def _auth_headers(self) -> dict[str, str]:
        api_key = request_api_key.get() or self._api_key
        bearer_token = request_bearer_token.get() or self._bearer_token
        if api_key:
            return {"x-iamcore-api-key": api_key}
        if bearer_token:
            return {"Authorization": f"Bearer {bearer_token}"}
        return {}

    async def request_response(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        headers: dict[str, str] | None = None,
        content_type: str | None = None,
    ) -> httpx.Response:
        base = (request_base_url.get() or self.base_url).rstrip("/")
        url = f"{base}{path}"
        hdrs = self._auth_headers()
        if headers:
            hdrs.update(headers)
        if content_type:
            hdrs["Content-Type"] = content_type

        resp = await self._client.request(
            method,
            url,
            params=params,
            json=json,
            headers=hdrs,
        )

        if resp.status_code in (401, 403):
            raise KaaAuthError(resp.status_code, resp.text)
        if resp.status_code == 404:
            raise KaaNotFoundError(resp.status_code, resp.text)
        if resp.status_code >= 400:
            raise KaaApiError(resp.status_code, resp.text)

        return resp

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        headers: dict[str, str] | None = None,
        content_type: str | None = None,
    ) -> Any:
        resp = await self.request_response(
            method,
            path,
            params=params,
            json=json,
            headers=headers,
            content_type=content_type,
        )

        if resp.status_code == 204:
            return None
        if resp.headers.get("content-type", "").startswith("application/json"):
            return resp.json()
        return resp.text

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> KaaClient:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()
