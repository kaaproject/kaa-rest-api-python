from __future__ import annotations

from typing import Any

from .client import KaaClient, request_tenant_id


def _clean(d: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in d.items() if v is not None}


class TektonClient:
    PREFIX = "/tekton/api/v1"

    def __init__(self, c: KaaClient):
        self._c = c

    # ------------------------------------------------------------------
    # Service instances
    # ------------------------------------------------------------------

    # 1. GET /service-instances
    async def list_service_instances(self) -> Any:
        return await self._c.request(
            "GET", f"{self.PREFIX}/service-instances",
        )

    # 2. GET /service-instances/{serviceInstanceName}
    async def get_service_instance(
        self, service_instance_name: str,
    ) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/service-instances/{service_instance_name}",
        )

    # ------------------------------------------------------------------
    # Applications
    # ------------------------------------------------------------------

    # 3. POST /applications
    async def create_application(
        self, body: dict[str, Any], *, tenant_id: str | None = None,
    ) -> Any:
        params = _clean({"tenantId": tenant_id or request_tenant_id.get()})
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/applications",
            json=body,
            params=params or None,
        )

    # 4. GET /applications
    async def list_applications(
        self, *, tenant_id: str | None = None,
    ) -> Any:
        params = _clean({"tenantId": tenant_id or request_tenant_id.get()})
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/applications",
            params=params or None,
        )

    # 5. GET /applications/{appName}
    async def get_application(
        self, app_name: str, *, tenant_id: str | None = None,
    ) -> Any:
        params = _clean({"tenantId": tenant_id or request_tenant_id.get()})
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/applications/{app_name}",
            params=params or None,
        )

    # 6. PATCH /applications/{appName}
    async def update_application(
        self, app_name: str, body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "PATCH",
            f"{self.PREFIX}/applications/{app_name}",
            json=body,
        )

    # ------------------------------------------------------------------
    # Application versions
    # ------------------------------------------------------------------

    # 7. POST /applications/{appName}/app-versions
    async def create_app_version(
        self, app_name: str, body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/applications/{app_name}/app-versions",
            json=body,
        )

    # 8. GET /applications/{appName}/app-versions
    async def list_app_versions(self, app_name: str) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/applications/{app_name}/app-versions",
        )

    # 9. GET /applications/{appName}/app-versions/{appVersionName}
    async def get_app_version(
        self, app_name: str, app_version_name: str,
    ) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/applications/{app_name}/app-versions/{app_version_name}",
        )

    # 10. PATCH /applications/{appName}/app-versions/{appVersionName}
    async def update_app_version(
        self, app_name: str, app_version_name: str, body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "PATCH",
            f"{self.PREFIX}/applications/{app_name}/app-versions/{app_version_name}",
            json=body,
        )

    # ------------------------------------------------------------------
    # Application configurations
    # ------------------------------------------------------------------

    # 11. POST /app-configs
    async def init_app_configs(self, body: dict[str, Any]) -> Any:
        return await self._c.request(
            "POST", f"{self.PREFIX}/app-configs", json=body,
        )

    # 12. GET /app-configs
    async def export_app_configs(
        self, *, service_instance_name: str | None = None,
    ) -> Any:
        params = _clean({"serviceInstanceName": service_instance_name})
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/app-configs",
            params=params or None,
        )

    # 13. PUT /app-configs/applications/{appName}
    async def upsert_app_config(
        self, app_name: str, body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/app-configs/applications/{app_name}",
            json=body,
        )

    # 14. GET /app-configs/applications/{appName}
    async def get_app_config(
        self, app_name: str, *, service_instance_name: str | None = None,
    ) -> Any:
        params = _clean({"serviceInstanceName": service_instance_name})
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/app-configs/applications/{app_name}",
            params=params or None,
        )

    # 15. PATCH /app-configs/applications/{appName}
    async def patch_app_config(
        self, app_name: str, service_instance_name: str,
        body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "PATCH",
            f"{self.PREFIX}/app-configs/applications/{app_name}",
            params={"serviceInstanceName": service_instance_name},
            json=body,
        )

    # ------------------------------------------------------------------
    # Application version configurations
    # ------------------------------------------------------------------

    # 16. PUT /app-configs/applications/{appName}/app-versions/{appVersionName}
    async def upsert_app_version_config(
        self, app_name: str, app_version_name: str, body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/app-configs/applications/{app_name}/app-versions/{app_version_name}",
            json=body,
        )

    # 17. GET /app-configs/applications/{appName}/app-versions/{appVersionName}
    async def get_app_version_config(
        self, app_name: str, app_version_name: str,
        *, service_instance_name: str | None = None,
    ) -> Any:
        params = _clean({"serviceInstanceName": service_instance_name})
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/app-configs/applications/{app_name}/app-versions/{app_version_name}",
            params=params or None,
        )

    # 18. PATCH /app-configs/applications/{appName}/app-versions/{appVersionName}
    async def patch_app_version_config(
        self, app_name: str, app_version_name: str,
        service_instance_name: str, body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "PATCH",
            f"{self.PREFIX}/app-configs/applications/{app_name}/app-versions/{app_version_name}",
            params={"serviceInstanceName": service_instance_name},
            json=body,
        )

    # ------------------------------------------------------------------
    # Tenant configurations
    # ------------------------------------------------------------------

    # 19. PUT /tenant-configs
    async def upsert_tenant_config(self, body: dict[str, Any]) -> Any:
        return await self._c.request(
            "PUT", f"{self.PREFIX}/tenant-configs", json=body,
        )

    # 20. GET /tenant-configs
    async def get_tenant_configs(
        self,
        *,
        service_instance_name: str | None = None,
        tenant_id: str | None = None,
    ) -> Any:
        params = _clean({
            "serviceInstanceName": service_instance_name,
            "tenantId": tenant_id or request_tenant_id.get(),
        })
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/tenant-configs",
            params=params or None,
        )

    # ------------------------------------------------------------------
    # Bulk export
    # ------------------------------------------------------------------

    # 21. GET /bulk
    async def bulk_export(
        self,
        *,
        service_instance_name: str | None = None,
        include: str | None = None,
        app_name: str | None = None,
    ) -> Any:
        params = _clean({
            "serviceInstanceName": service_instance_name,
            "include": include,
            "appName": app_name,
        })
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/bulk",
            params=params or None,
        )
