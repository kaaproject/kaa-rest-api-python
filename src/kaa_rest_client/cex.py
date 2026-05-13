from __future__ import annotations

from typing import Any

from .client import KaaClient


def _clean(d: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in d.items() if v is not None}


class CexClient:
    PREFIX = "/cex/api/v1"

    def __init__(self, c: KaaClient):
        self._c = c

    # 1. POST /endpoints/{endpointId}/commands/{commandType}
    async def invoke_command(
        self,
        endpoint_id: str,
        command_type: str,
        body: dict[str, Any] | None = None,
        *,
        await_timeout: int | None = None,
    ) -> Any:
        params = _clean({"awaitTimeout": await_timeout})
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/endpoints/{endpoint_id}/commands/{command_type}",
            params=params or None,
            json=body,
        )

    # 2. GET /endpoints/{endpointId}/commands/{commandType}/{commandId}
    async def get_command(
        self,
        endpoint_id: str,
        command_type: str,
        command_id: str,
    ) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/endpoints/{endpoint_id}/commands/{command_type}/{command_id}",
        )

    # 3. DELETE /endpoints/{endpointId}/commands/{commandType}/{commandId}
    async def delete_command(
        self,
        endpoint_id: str,
        command_type: str,
        command_id: str,
    ) -> Any:
        return await self._c.request(
            "DELETE",
            f"{self.PREFIX}/endpoints/{endpoint_id}/commands/{command_type}/{command_id}",
        )

    # 4. GET /endpoints/{endpointId}/commands/{commandType}/last
    async def get_last_command(
        self,
        endpoint_id: str,
        command_type: str,
    ) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/endpoints/{endpoint_id}/commands/{command_type}/last",
        )

    # 5. GET /endpoints/commands
    async def list_commands_for_endpoints(
        self,
        endpoint_id: str,
        *,
        command_types: str | None = None,
    ) -> Any:
        params = _clean({
            "endpointId": endpoint_id,
            "commandTypes": command_types,
        })
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/endpoints/commands",
            params=params or None,
        )

    # 6. GET /endpoints/commands/{applicationName}
    async def list_commands_for_app(
        self,
        application_name: str,
        *,
        page: int | None = None,
        sort: str | None = None,
        size: int | None = None,
        command_types: str | None = None,
    ) -> Any:
        params = _clean({
            "page": page,
            "sort": sort,
            "size": size,
            "commandTypes": command_types,
        })
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/endpoints/commands/{application_name}",
            params=params or None,
        )

    # 7. POST /endpoints/commands/last
    async def get_last_commands_bulk(
        self,
        endpoint_ids: list[str],
        command_types: list[str],
    ) -> Any:
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/endpoints/commands/last",
            json={
                "endpointIds": endpoint_ids,
                "commandTypes": command_types,
            },
        )

    # 8. POST /endpoints/commands/{commandType}/batch/by-filter
    async def batch_command_by_filter(
        self,
        command_type: str,
        filter_id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/endpoints/commands/{command_type}/batch/by-filter",
            params={"filterId": filter_id},
            json=body,
        )

    # 9. POST /endpoints/commands/{commandType}/batch/by-endpoints
    async def batch_command_by_endpoints(
        self,
        command_type: str,
        payload: dict[str, Any],
        endpoint_ids: list[str],
        *,
        payload_content_type: str | None = None,
    ) -> Any:
        body = _clean({
            "payload": payload,
            "payloadContentType": payload_content_type,
            "endpointIds": endpoint_ids,
        })
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/endpoints/commands/{command_type}/batch/by-endpoints",
            json=body,
        )

    # 10. GET /endpoints/commands/batch/tasks
    async def list_batch_tasks(
        self,
        app_name: str,
        *,
        command_type: str | None = None,
        filter_id: str | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> Any:
        params = _clean({
            "appName": app_name,
            "commandType": command_type,
            "filterId": filter_id,
            "sortBy": sort_by,
            "sortOrder": sort_order,
            "offset": offset,
            "limit": limit,
        })
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/endpoints/commands/batch/tasks",
            params=params or None,
        )

    # 11. GET /endpoints/commands/batch/tasks/{id}
    async def get_batch_task_status(
        self,
        task_id: str,
        app_name: str,
    ) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/endpoints/commands/batch/tasks/{task_id}",
            params={"appName": app_name},
        )
