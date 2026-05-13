from __future__ import annotations

from typing import Any

from .client import KaaClient, request_tenant_id


def _clean(d: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in d.items() if v is not None}


class EprClient:
    PREFIX = "/epr/api/v1"

    def __init__(self, c: KaaClient):
        self._c = c

    # ── Endpoints ─────────────────────────────────────────────────────

    async def register_endpoint(self, body: dict[str, Any]) -> dict[str, Any]:
        """POST /endpoints - Register a new endpoint."""
        return await self._c.request("POST", f"{self.PREFIX}/endpoints", json=body)

    async def list_endpoints(
        self,
        *,
        endpoint_id: str | None = None,
        application_name: str | None = None,
        application_version_name: str | None = None,
        tenant_id: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
        metadata_filter: str | None = None,
        multi_filter: str | None = None,
        regex: str | None = None,
        filter_id: str | None = None,
        include: str | None = None,
    ) -> dict[str, Any]:
        """GET /endpoints - List endpoints."""
        params = _clean(
            {
                "endpointId": endpoint_id,
                "applicationName": application_name,
                "applicationVersionName": application_version_name,
                "tenantId": tenant_id or request_tenant_id.get(),
                "offset": offset,
                "limit": limit,
                "metadataFilter": metadata_filter,
                "multiFilter": multi_filter,
                "regex": regex,
                "filterId": filter_id,
                "include": include,
            }
        )
        return await self._c.request("GET", f"{self.PREFIX}/endpoints", params=params)

    async def search_endpoints(self, body: dict[str, Any]) -> dict[str, Any]:
        """POST /endpoints/search - Search endpoints with filters."""
        return await self._c.request(
            "POST", f"{self.PREFIX}/endpoints/search", json=body
        )

    async def batch_delete_endpoints(self, body: dict[str, Any]) -> dict[str, Any]:
        """POST /endpoints/delete - Batch delete endpoints."""
        return await self._c.request(
            "POST", f"{self.PREFIX}/endpoints/delete", json=body
        )

    async def batch_register_endpoints(self, body: dict[str, Any]) -> dict[str, Any]:
        """POST /endpoints/batch - Batch register endpoints."""
        return await self._c.request(
            "POST", f"{self.PREFIX}/endpoints/batch", json=body
        )

    async def get_batch_registration_status(
        self,
        app_name: str,
        task_id: str,
    ) -> dict[str, Any]:
        """GET /endpoints/batch/status - Get batch registration status."""
        params = {"appName": app_name, "taskId": task_id}
        return await self._c.request(
            "GET", f"{self.PREFIX}/endpoints/batch/status", params=params
        )

    async def get_endpoint(
        self,
        endpoint_id: str,
        *,
        tenant_id: str | None = None,
    ) -> dict[str, Any]:
        """GET /endpoints/{endpointId} - Get a single endpoint."""
        params = _clean({"tenantId": tenant_id or request_tenant_id.get()})
        params["include"] = (
            "metadata"  # metadata is not included by default but is often needed, so include it by default
        )
        return await self._c.request(
            "GET", f"{self.PREFIX}/endpoints/{endpoint_id}", params=params
        )

    async def delete_endpoint(self, endpoint_id: str) -> Any:
        """DELETE /endpoints/{endpointId} - Delete an endpoint."""
        return await self._c.request("DELETE", f"{self.PREFIX}/endpoints/{endpoint_id}")

    # ── Endpoint relations ────────────────────────────────────────────

    async def get_endpoint_relations(
        self,
        endpoint_id: str,
        relation: str,
    ) -> dict[str, Any]:
        """GET /endpoints/{endpointId}/relations - Get endpoint relations."""
        params = {"relation": relation}
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/endpoints/{endpoint_id}/relations",
            params=params,
        )

    # ── Endpoint app version ──────────────────────────────────────────

    async def get_endpoint_app_version(self, endpoint_id: str) -> dict[str, Any]:
        """GET /endpoints/{endpointId}/app-version - Get endpoint app version."""
        return await self._c.request(
            "GET", f"{self.PREFIX}/endpoints/{endpoint_id}/app-version"
        )

    async def update_endpoint_app_version(
        self,
        endpoint_id: str,
        body: dict[str, Any],
    ) -> dict[str, Any]:
        """PUT /endpoints/{endpointId}/app-version - Update endpoint app version."""
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/endpoints/{endpoint_id}/app-version",
            json=body,
        )

    # ── Endpoint metadata ─────────────────────────────────────────────

    async def get_endpoint_metadata(
        self,
        endpoint_id: str,
        *,
        include: str | None = None,
    ) -> dict[str, Any]:
        """GET /endpoints/{endpointId}/metadata - Get endpoint metadata."""
        params = _clean({"include": include})
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/endpoints/{endpoint_id}/metadata",
            params=params,
        )

    async def update_endpoint_metadata(
        self,
        endpoint_id: str,
        body: dict[str, Any],
        *,
        inherited_metadata: str | None = None,
    ) -> dict[str, Any]:
        """PUT /endpoints/{endpointId}/metadata - Full update of endpoint metadata."""
        params = _clean({"inheritedMetadata": inherited_metadata})
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/endpoints/{endpoint_id}/metadata",
            params=params,
            json=body,
        )

    async def patch_endpoint_metadata(
        self,
        endpoint_id: str,
        body: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """PATCH /endpoints/{endpointId}/metadata - JSON Patch on endpoint metadata."""
        return await self._c.request(
            "PATCH",
            f"{self.PREFIX}/endpoints/{endpoint_id}/metadata",
            json=body,
            content_type="application/json-patch+json",
        )

    async def get_endpoint_metadata_key(
        self,
        endpoint_id: str,
        metadata_key: str,
    ) -> Any:
        """GET /endpoints/{endpointId}/metadata/{metadataKey} - Get a single metadata key."""
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/endpoints/{endpoint_id}/metadata/{metadata_key}",
        )

    async def update_endpoint_metadata_key(
        self,
        endpoint_id: str,
        metadata_key: str,
        body: Any,
    ) -> Any:
        """PUT /endpoints/{endpointId}/metadata/{metadataKey} - Update a single metadata key."""
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/endpoints/{endpoint_id}/metadata/{metadata_key}",
            json=body,
        )

    async def delete_endpoint_metadata_key(
        self,
        endpoint_id: str,
        metadata_key: str,
    ) -> Any:
        """DELETE /endpoints/{endpointId}/metadata/{metadataKey} - Delete a single metadata key."""
        return await self._c.request(
            "DELETE",
            f"{self.PREFIX}/endpoints/{endpoint_id}/metadata/{metadata_key}",
        )

    async def get_endpoint_metadata_keys(self, endpoint_id: str) -> list[str]:
        """GET /endpoints/{endpointId}/metadata-keys - Get all metadata key names.

        connected and connectivity_ts are always injected so callers can rely
        on their presence regardless of whether the device has ever connected.
        """
        result = await self._c.request(
            "GET",
            f"{self.PREFIX}/endpoints/{endpoint_id}/metadata-keys",
        )
        if isinstance(result, list):
            for key in ("connected", "connectivity_ts"):
                if key not in result:
                    result.append(key)
        return result

    # ── Application filters ──────────────────────────────────────────

    async def list_filters(
        self,
        application_name: str,
        *,
        name: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """GET /applications/{applicationName}/filters - List filters."""
        params = _clean({"name": name, "offset": offset, "limit": limit})
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/applications/{application_name}/filters",
            params=params,
        )

    async def create_filter(
        self,
        application_name: str,
        body: dict[str, Any],
    ) -> dict[str, Any]:
        """POST /applications/{applicationName}/filters - Create a filter."""
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/applications/{application_name}/filters",
            json=body,
        )

    async def get_filter(
        self,
        application_name: str,
        filter_id: str,
    ) -> dict[str, Any]:
        """GET /applications/{applicationName}/filters/{filterId} - Get a filter."""
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/applications/{application_name}/filters/{filter_id}",
        )

    async def update_filter(
        self,
        application_name: str,
        filter_id: str,
        body: dict[str, Any],
        *,
        if_match: str | None = None,
    ) -> dict[str, Any]:
        """PATCH /applications/{applicationName}/filters/{filterId} - Update a filter."""
        headers = _clean({"If-Match": if_match})
        return await self._c.request(
            "PATCH",
            f"{self.PREFIX}/applications/{application_name}/filters/{filter_id}",
            json=body,
            headers=headers or None,
        )

    async def delete_filter(
        self,
        application_name: str,
        filter_id: str,
        *,
        if_match: str | None = None,
    ) -> Any:
        """DELETE /applications/{applicationName}/filters/{filterId} - Delete a filter."""
        headers = _clean({"If-Match": if_match})
        return await self._c.request(
            "DELETE",
            f"{self.PREFIX}/applications/{application_name}/filters/{filter_id}",
            headers=headers or None,
        )

    # ── Application metadata keys ────────────────────────────────────

    async def get_app_metadata_keys(self, application_name: str) -> dict[str, Any]:
        """GET /applications/{applicationName}/metadata-keys - Get app-level metadata keys."""
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/applications/{application_name}/metadata-keys",
        )

    # ── Relations ─────────────────────────────────────────────────────

    async def link_endpoints(self, body: list[dict[str, Any]]) -> dict[str, Any]:
        """PUT /relations/link - Link endpoints by relations."""
        return await self._c.request("PUT", f"{self.PREFIX}/relations/link", json=body)

    async def unlink_endpoints(self, body: list[dict[str, Any]]) -> dict[str, Any]:
        """PUT /relations/unlink - Unlink endpoints by relations."""
        return await self._c.request(
            "PUT", f"{self.PREFIX}/relations/unlink", json=body
        )
