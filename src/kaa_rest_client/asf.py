from __future__ import annotations

from typing import Any

from .client import KaaClient, request_tenant_id


class AsfClient:
    PREFIX = "/asf/api/v1"

    def __init__(self, c: KaaClient):
        self._c = c

    @staticmethod
    def _resolve_tenant(tenant_id: str | None) -> str:
        tid = tenant_id or request_tenant_id.get()
        if not tid:
            raise ValueError("tenant_id is required (pass explicitly or set via query parameter)")
        return tid

    # ── Ingest pipelines ───────────────────────────────────────────────

    # 1. PUT /_ingest/pipeline/{pipelineID}
    async def upsert_pipeline(
        self,
        pipeline_id: str,
        body: dict[str, Any],
    ) -> dict[str, Any]:
        """Create or update an ingest pipeline."""
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/_ingest/pipeline/{pipeline_id}",
            json=body,
        )

    # 2. GET /_ingest/pipeline/{pipelineID}
    async def get_pipeline(self, pipeline_id: str) -> dict[str, Any]:
        """Retrieve a pipeline by ID."""
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/_ingest/pipeline/{pipeline_id}",
        )

    # 3. DELETE /_ingest/pipeline/{pipelineID}
    async def delete_pipeline(self, pipeline_id: str) -> dict[str, Any]:
        """Delete a pipeline by ID."""
        return await self._c.request(
            "DELETE",
            f"{self.PREFIX}/_ingest/pipeline/{pipeline_id}",
        )

    # 4. POST /_ingest/pipeline/simulate/{pipelineID}
    async def simulate_pipeline_by_id(
        self,
        pipeline_id: str,
        body: dict[str, Any],
    ) -> dict[str, Any]:
        """Simulate a pipeline by ID with provided documents."""
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/_ingest/pipeline/simulate/{pipeline_id}",
            json=body,
        )

    # 5. POST /_ingest/pipeline/simulate/
    async def simulate_pipeline(
        self,
        body: dict[str, Any],
    ) -> dict[str, Any]:
        """Simulate a pipeline with inline pipeline definition and documents."""
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/_ingest/pipeline/simulate/",
            json=body,
        )

    # ── Templates and mappings ─────────────────────────────────────────

    # 6. PUT /{tenantID}-{applicationName}-{date}/_template
    async def upsert_template(
        self,
        application_name: str,
        body: dict[str, Any],
        date: str = "*",
        *,
        tenant_id: str | None = None,
    ) -> dict[str, Any]:
        """Create or update an index template."""
        tid = self._resolve_tenant(tenant_id)
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/{tid}-{application_name}-{date}/_template",
            json=body,
        )

    # 7. GET /{tenantID}-{applicationName}-{date}/_template
    async def get_template(
        self,
        application_name: str,
        date: str = "*",
        *,
        tenant_id: str | None = None,
    ) -> dict[str, Any]:
        """Retrieve an index template."""
        tid = self._resolve_tenant(tenant_id)
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/{tid}-{application_name}-{date}/_template",
        )

    # 8. GET /{tenantID}-{applicationName}-{date}/_mapping
    async def get_mapping(
        self,
        application_name: str,
        date: str = "*",
        *,
        tenant_id: str | None = None,
    ) -> dict[str, Any]:
        """Retrieve index mappings."""
        tid = self._resolve_tenant(tenant_id)
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/{tid}-{application_name}-{date}/_mapping",
        )

    # ── Search ─────────────────────────────────────────────────────────

    # 9. POST /{tenantID}-kaa-system-traffic-statistics/_search
    async def search_traffic_statistics(
        self,
        body: dict[str, Any],
        *,
        tenant_id: str | None = None,
    ) -> dict[str, Any]:
        """Search traffic statistics for a tenant."""
        tid = self._resolve_tenant(tenant_id)
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/{tid}-kaa-system-traffic-statistics/_search",
            json=body,
        )

    # 10. POST /{tenantID}-{applicationName}-{date}/_search
    async def search_documents(
        self,
        application_name: str,
        body: dict[str, Any],
        date: str = "*",
        *,
        tenant_id: str | None = None,
    ) -> dict[str, Any]:
        """Search documents in a date-specific index."""
        tid = self._resolve_tenant(tenant_id)
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/{tid}-{application_name}-{date}/_search",
            json=body,
        )

    # 11. POST /{tenantID}-{applicationName}-{date}/_msearch
    async def multi_search_documents(
        self,
        application_name: str,
        body: dict[str, Any],
        date: str = "*",
        *,
        tenant_id: str | None = None,
    ) -> dict[str, Any]:
        """Execute multiple search requests in a single API call."""
        tid = self._resolve_tenant(tenant_id)
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/{tid}-{application_name}-{date}/_msearch",
            json=body,
        )
