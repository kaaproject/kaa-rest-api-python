from __future__ import annotations

from typing import Any

from .client import KaaClient


def _clean(d: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in d.items() if v is not None}


class TenantManagerClient:
    PREFIX = "/api/v2"

    def __init__(self, c: KaaClient):
        self._c = c

    # ── Tenants ───────────────────────────────────────────────────────

    async def list_tenants(
        self,
        *,
        tenant_id: str | None = None,
        name: str | None = None,
        admin: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> Any:
        """GET /tenants - List tenants accessible to the authenticated user."""
        params = _clean(
            {
                "tenant_id": tenant_id,
                "name": name,
                "admin": admin,
                "offset": offset,
                "limit": limit,
            }
        )
        return await self._c.request("GET", f"{self.PREFIX}/tenants", params=params or None)

    async def create_tenant(self, body: dict[str, Any]) -> Any:
        """POST /tenants - Create a new tenant."""
        return await self._c.request("POST", f"{self.PREFIX}/tenants", json=body)

    async def get_tenant(self, tenant_pk: str) -> Any:
        """GET /tenants/{tenant_pk} - Get a tenant by its internal UUID."""
        return await self._c.request("GET", f"{self.PREFIX}/tenants/{tenant_pk}")

    async def update_tenant(self, tenant_pk: str, body: dict[str, Any]) -> Any:
        """PUT /tenants/{tenant_pk} - Update tenant information."""
        return await self._c.request(
            "PUT", f"{self.PREFIX}/tenants/{tenant_pk}", json=body
        )

    async def delete_tenant(self, tenant_pk: str) -> Any:
        """DELETE /tenants/{tenant_pk} - Delete a tenant and all its resources."""
        return await self._c.request("DELETE", f"{self.PREFIX}/tenants/{tenant_pk}")

    async def get_tenant_credentials(self, tenant_pk: str) -> Any:
        """GET /tenants/{tenant_pk}/credentials - Get OAuth and service credentials."""
        return await self._c.request(
            "GET", f"{self.PREFIX}/tenants/{tenant_pk}/credentials"
        )

    # ── Package Types ─────────────────────────────────────────────────

    async def list_package_types(self) -> Any:
        """GET /packages-types - List all available package types."""
        return await self._c.request("GET", f"{self.PREFIX}/packages-types")

    async def get_package_type(self, pk: str) -> Any:
        """GET /packages-types/{pk} - Get a package type by ID."""
        return await self._c.request("GET", f"{self.PREFIX}/packages-types/{pk}")

    # ── Subscriptions ─────────────────────────────────────────────────

    async def list_subscriptions(
        self,
        tenant_id: str,
        *,
        offset: int | None = None,
        limit: int | None = None,
    ) -> Any:
        """GET /tenants-subscriptions - List subscriptions for a tenant."""
        params = _clean({"tenant_id": tenant_id, "offset": offset, "limit": limit})
        return await self._c.request(
            "GET", f"{self.PREFIX}/tenants-subscriptions", params=params
        )

    # ── Users (templates) ─────────────────────────────────────────────

    async def list_users(
        self,
        *,
        search: str | None = None,
        enabled: bool | None = None,
    ) -> Any:
        """GET /users - List user templates."""
        params = _clean({"search": search, "enabled": enabled})
        return await self._c.request("GET", f"{self.PREFIX}/users", params=params or None)

    async def create_user(self, body: dict[str, Any]) -> Any:
        """POST /users - Create a new user template."""
        return await self._c.request("POST", f"{self.PREFIX}/users", json=body)

    async def delete_user(self, pk: str) -> Any:
        """DELETE /users/{pk} - Delete a user template."""
        return await self._c.request("DELETE", f"{self.PREFIX}/users/{pk}")
