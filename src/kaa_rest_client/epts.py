from __future__ import annotations

from typing import Any

from .client import KaaClient


def _clean(d: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in d.items() if v is not None}


class EptsClient:
    PREFIX = "/epts"

    def __init__(self, c: KaaClient):
        self._c = c

    async def get_time_series_config(
        self,
        *,
        application_names: str | None = None,
    ) -> dict[str, Any]:
        params = _clean({"applicationNames": application_names})
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/api/v1/time-series/config",
            params=params or None,
        )

    async def get_last_time_series(
        self,
        application_name: str,
    ) -> dict[str, Any]:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/api/v1/applications/{application_name}/time-series/last",
        )

    async def get_last_time_series_with_filters(
        self,
        application_name: str,
        *,
        time_series_names: list[str] | None = None,
        before_date: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
        endpoint_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        body = _clean(
            {
                "timeSeriesNames": time_series_names,
                "beforeDate": before_date,
                "offset": offset,
                "limit": limit,
                "endpointIDs": endpoint_ids,
            }
        )
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/api/v1/applications/{application_name}/time-series/last",
            json=body or None,
        )

    async def get_time_series_data(
        self,
        application_name: str,
        *,
        time_series_name: str,
        from_date: str,
        to_date: str,
        endpoint_id: str | None = None,
        include_time: str | None = None,
        sort: str | None = None,
    ) -> Any:
        params = _clean(
            {
                "timeSeriesName": time_series_name,
                "endpointId": endpoint_id,
                "fromDate": from_date,
                "toDate": to_date,
                "includeTime": include_time,
                "sort": sort,
            }
        )
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/api/v1/applications/{application_name}/time-series/data",
            params=params,
        )
