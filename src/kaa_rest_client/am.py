from __future__ import annotations

from typing import Any

from .client import KaaClient


def _clean(d: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in d.items() if v is not None}


class AmClient:
    PREFIX = "/am/api/v1"
    PREFIX_V2 = "/am/api/v2"

    def __init__(self, c: KaaClient):
        self._c = c

    # ── Asset Types ───────────────────────────────────────────────────

    async def create_asset_type(self, body: dict[str, Any]) -> Any:
        """POST /asset-types - Create a new asset type."""
        return await self._c.request("POST", f"{self.PREFIX}/asset-types", json=body)

    async def list_asset_types(
        self,
        *,
        type: str | None = None,
        description: str | None = None,
    ) -> Any:
        """GET /asset-types - List asset types."""
        params = _clean({"type": type, "description": description})
        return await self._c.request(
            "GET", f"{self.PREFIX}/asset-types", params=params or None
        )

    async def get_asset_type(self, asset_type_id: str) -> Any:
        """GET /asset-types/{assetTypeId} - Get an asset type by ID."""
        return await self._c.request(
            "GET", f"{self.PREFIX}/asset-types/{asset_type_id}"
        )

    async def update_asset_type(
        self, asset_type_id: str, body: dict[str, Any]
    ) -> Any:
        """PUT /asset-types/{assetTypeId} - Update an asset type."""
        return await self._c.request(
            "PUT", f"{self.PREFIX}/asset-types/{asset_type_id}", json=body
        )

    async def delete_asset_type(self, asset_type_id: str) -> Any:
        """DELETE /asset-types/{assetTypeId} - Delete an asset type."""
        return await self._c.request(
            "DELETE", f"{self.PREFIX}/asset-types/{asset_type_id}"
        )

    # ── Assets ────────────────────────────────────────────────────────

    async def create_asset(self, body: dict[str, Any]) -> Any:
        """POST /assets - Create a new asset."""
        return await self._c.request("POST", f"{self.PREFIX}/assets", json=body)

    async def list_assets(self, body: dict[str, Any] | None = None) -> Any:
        """POST /assets/list - List assets with optional filtering."""
        return await self._c.request(
            "POST", f"{self.PREFIX}/assets/list", json=body or {}
        )

    async def get_asset(self, asset_id: str) -> Any:
        """GET /assets/{assetId} - Get an asset by ID."""
        return await self._c.request("GET", f"{self.PREFIX}/assets/{asset_id}")

    async def update_asset(self, asset_id: str, body: dict[str, Any]) -> Any:
        """PUT /assets/{assetId} - Update an asset."""
        return await self._c.request(
            "PUT", f"{self.PREFIX}/assets/{asset_id}", json=body
        )

    async def patch_asset(self, asset_id: str, body: dict[str, Any]) -> Any:
        """PATCH /assets/{assetId} - Patch an asset (RFC 6902 operations)."""
        return await self._c.request(
            "PATCH", f"{self.PREFIX}/assets/{asset_id}", json=body
        )

    async def delete_asset(self, asset_id: str) -> Any:
        """DELETE /assets/{assetId} - Delete an asset."""
        return await self._c.request("DELETE", f"{self.PREFIX}/assets/{asset_id}")

    # ── Relations ─────────────────────────────────────────────────────

    async def get_relations(self, entity_ids: str) -> Any:
        """GET /api/v2/relations - Get relations for entity IDs."""
        return await self._c.request(
            "GET", f"{self.PREFIX_V2}/relations", params={"entityIds": entity_ids}
        )

    async def link_entities(self, body: dict[str, Any]) -> Any:
        """POST /relations/link - Create a relation between entities."""
        return await self._c.request(
            "POST", f"{self.PREFIX}/relations/link", json=body
        )

    async def unlink_entities(self, body: dict[str, Any]) -> Any:
        """POST /relations/unlink - Delete a relation between entities."""
        return await self._c.request(
            "POST", f"{self.PREFIX}/relations/unlink", json=body
        )

    async def get_relation_sessions(self, entity_id: str) -> Any:
        """GET /relation-sessions - Get relation sessions for an entity."""
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/relation-sessions",
            params={"entityId": entity_id},
        )

    async def get_relation_tree(self, entity_type: str, entity_id: str) -> Any:
        """GET /relation-trees - Get relation tree for an entity."""
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/relation-trees",
            params={"entityType": entity_type, "entityId": entity_id},
        )
