from __future__ import annotations

import json
from typing import Any, Callable, Mapping, Optional

import httpx

from .client import KaaClient
from .ecr_models import (
    BulkConfigurationRequest,
    ConfigurationStatusPage,
    EndpointConfiguration,
    EcrResponse,
    JsonValue,
    SystemConfiguration,
    SystemConfigurationInput,
    SystemConfigurationList,
)


def _clean(params: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value is not None}


def _decode_response(response: httpx.Response) -> Any:
    if response.status_code == 204 or not response.content:
        return None
    if response.headers.get("content-type", "").startswith("application/json"):
        return response.json()
    return response.text


def _to_payload(body: Any) -> Any:
    to_payload = getattr(body, "to_payload", None)
    return to_payload() if callable(to_payload) else body


def _system_body(body: Any) -> Any:
    if isinstance(body, SystemConfigurationInput):
        return body.to_payload()
    if not isinstance(body, Mapping):
        return _to_payload(body)

    payload = dict(body)
    if "display_name" in payload and "displayName" not in payload:
        payload["displayName"] = payload.pop("display_name")
    if "config" in payload and not isinstance(payload["config"], str):
        payload["config"] = json.dumps(payload["config"])
    return payload


def _endpoint_configuration(value: Any) -> EndpointConfiguration:
    return EndpointConfiguration.from_dict(value)


def _endpoint_configurations(value: Any) -> list[EndpointConfiguration]:
    return [EndpointConfiguration.from_dict(item) for item in value]


def _configuration_status_page(value: Any) -> ConfigurationStatusPage:
    return ConfigurationStatusPage.from_dict(value)


def _system_configuration(value: Any) -> SystemConfiguration:
    return SystemConfiguration.from_dict(value)


def _system_configurations(value: Any) -> SystemConfigurationList:
    return SystemConfigurationList.from_dict(value)


class EcrClient:
    PREFIX = "/ecr/api/v1"

    def __init__(self, c: KaaClient):
        self._c = c

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        body: Any = None,
        parser: Optional[Callable[[Any], Any]] = None,
    ) -> EcrResponse[Any]:
        response = await self._c.request_response(
            method,
            path,
            params=params,
            json=_to_payload(body),
        )
        data = _decode_response(response)
        if parser is not None and data is not None:
            data = parser(data)
        return EcrResponse(
            data=data,
            status_code=response.status_code,
            headers=dict(response.headers.items()),
        )

    # ------------------------------------------------------------------
    # Endpoint-delivered configuration
    # ------------------------------------------------------------------

    async def upsert_endpoint_configuration(
        self,
        endpoint_id: str,
        app_version_name: str,
        body: JsonValue,
    ) -> EcrResponse[EndpointConfiguration]:
        return await self._request(
            "PUT",
            f"{self.PREFIX}/endpoints/{endpoint_id}/app-versions/{app_version_name}",
            body=body,
            parser=_endpoint_configuration,
        )

    async def get_endpoint_configuration(
        self,
        endpoint_id: str,
        app_version_name: str,
    ) -> EcrResponse[EndpointConfiguration]:
        return await self._request(
            "GET",
            f"{self.PREFIX}/endpoints/{endpoint_id}/app-versions/{app_version_name}",
            parser=_endpoint_configuration,
        )

    async def delete_endpoint_configuration(
        self,
        endpoint_id: str,
        app_version_name: str,
    ) -> EcrResponse[None]:
        return await self._request(
            "DELETE",
            f"{self.PREFIX}/endpoints/{endpoint_id}/app-versions/{app_version_name}",
        )

    async def list_endpoint_configurations(
        self,
        endpoint_id: str,
        app_version_name: str,
    ) -> EcrResponse[list[EndpointConfiguration]]:
        return await self._request(
            "GET",
            f"{self.PREFIX}/endpoints/{endpoint_id}/app-versions/{app_version_name}/configurations",
            parser=_endpoint_configurations,
        )

    async def bulk_upsert_endpoint_configurations(
        self,
        body: BulkConfigurationRequest | Mapping[str, Any],
    ) -> EcrResponse[None]:
        return await self._request(
            "PUT",
            f"{self.PREFIX}/endpoints/batch",
            body=body,
        )

    async def upsert_endpoint_configurations_by_filter(
        self,
        filter_id: str,
        body: JsonValue,
    ) -> EcrResponse[None]:
        return await self._request(
            "PUT",
            f"{self.PREFIX}/endpoints/filters/{filter_id}",
            body=body,
        )

    async def upsert_app_version_configuration(
        self,
        app_version_name: str,
        body: JsonValue,
    ) -> EcrResponse[EndpointConfiguration]:
        return await self._request(
            "PUT",
            f"{self.PREFIX}/app-versions/{app_version_name}",
            body=body,
            parser=_endpoint_configuration,
        )

    async def get_app_version_configuration(
        self,
        app_version_name: str,
    ) -> EcrResponse[EndpointConfiguration]:
        return await self._request(
            "GET",
            f"{self.PREFIX}/app-versions/{app_version_name}",
            parser=_endpoint_configuration,
        )

    async def delete_app_version_configuration(
        self,
        app_version_name: str,
    ) -> EcrResponse[None]:
        return await self._request(
            "DELETE",
            f"{self.PREFIX}/app-versions/{app_version_name}",
        )

    async def list_app_version_configurations(
        self,
        app_version_name: str,
    ) -> EcrResponse[list[EndpointConfiguration]]:
        return await self._request(
            "GET",
            f"{self.PREFIX}/app-versions/{app_version_name}/configurations",
            parser=_endpoint_configurations,
        )

    async def get_app_version_schema(
        self,
        app_version_name: str,
    ) -> EcrResponse[dict[str, Any]]:
        return await self._request(
            "GET",
            f"{self.PREFIX}/app-versions/{app_version_name}/schemas",
        )

    async def validate_app_version_schema(
        self,
        app_version_name: str,
        body: JsonValue,
    ) -> EcrResponse[None]:
        return await self._request(
            "PUT",
            f"{self.PREFIX}/app-versions/{app_version_name}/schemas/validate",
            body=body,
        )

    async def list_configuration_statuses(
        self,
        endpoint_id: str,
        *,
        app_version_name: Optional[str] = None,
        config_id: Optional[str] = None,
    ) -> EcrResponse[ConfigurationStatusPage]:
        params = _clean({
            "endpointId": endpoint_id,
            "appVersionName": app_version_name,
            "configId": config_id,
        })
        return await self._request(
            "GET",
            f"{self.PREFIX}/statuses",
            params=params,
            parser=_configuration_status_page,
        )

    # ------------------------------------------------------------------
    # System configuration
    #
    # These APIs are primarily for static defaults and platform-side
    # configuration. Updates are not directly shipped to devices over MQTT.
    # ------------------------------------------------------------------

    async def create_tenant_config(
        self,
        tenant_id: str,
        body: SystemConfigurationInput | Mapping[str, Any],
    ) -> EcrResponse[None]:
        return await self._request(
            "POST",
            f"{self.PREFIX}/system/tenants/{tenant_id}/configs",
            body=_system_body(body),
        )

    async def list_tenant_configs(
        self,
        tenant_id: str,
    ) -> EcrResponse[SystemConfigurationList]:
        return await self._request(
            "GET",
            f"{self.PREFIX}/system/tenants/{tenant_id}/configs",
            parser=_system_configurations,
        )

    async def get_current_tenant_config(
        self,
        tenant_id: str,
    ) -> EcrResponse[SystemConfiguration]:
        return await self._request(
            "GET",
            f"{self.PREFIX}/system/tenants/{tenant_id}/configs/current",
            parser=_system_configuration,
        )

    async def get_tenant_config(
        self,
        tenant_id: str,
        config_id: str,
    ) -> EcrResponse[SystemConfiguration]:
        return await self._request(
            "GET",
            f"{self.PREFIX}/system/tenants/{tenant_id}/configs/{config_id}",
            parser=_system_configuration,
        )

    async def update_tenant_config(
        self,
        tenant_id: str,
        config_id: str,
        body: SystemConfigurationInput | Mapping[str, Any],
    ) -> EcrResponse[None]:
        return await self._request(
            "PUT",
            f"{self.PREFIX}/system/tenants/{tenant_id}/configs/{config_id}",
            body=_system_body(body),
        )

    async def delete_tenant_config(
        self,
        tenant_id: str,
        config_id: str,
    ) -> EcrResponse[None]:
        return await self._request(
            "DELETE",
            f"{self.PREFIX}/system/tenants/{tenant_id}/configs/{config_id}",
        )

    async def create_application_config(
        self,
        app_name: str,
        body: SystemConfigurationInput | Mapping[str, Any],
    ) -> EcrResponse[None]:
        return await self._request(
            "POST",
            f"{self.PREFIX}/system/applications/{app_name}/configs",
            body=_system_body(body),
        )

    async def list_application_configs(
        self,
        app_name: str,
    ) -> EcrResponse[SystemConfigurationList]:
        return await self._request(
            "GET",
            f"{self.PREFIX}/system/applications/{app_name}/configs",
            parser=_system_configurations,
        )

    async def get_current_application_config(
        self,
        app_name: str,
        *,
        tree_traversal_strategy: Optional[str] = None,
    ) -> EcrResponse[SystemConfiguration]:
        params = _clean({"treeTraversalStrategy": tree_traversal_strategy})
        return await self._request(
            "GET",
            f"{self.PREFIX}/system/applications/{app_name}/configs/current",
            params=params,
            parser=_system_configuration,
        )

    async def get_application_config(
        self,
        app_name: str,
        config_id: str,
    ) -> EcrResponse[SystemConfiguration]:
        return await self._request(
            "GET",
            f"{self.PREFIX}/system/applications/{app_name}/configs/{config_id}",
            parser=_system_configuration,
        )

    async def update_application_config(
        self,
        app_name: str,
        config_id: str,
        body: SystemConfigurationInput | Mapping[str, Any],
    ) -> EcrResponse[None]:
        return await self._request(
            "PUT",
            f"{self.PREFIX}/system/applications/{app_name}/configs/{config_id}",
            body=_system_body(body),
        )

    async def delete_application_config(
        self,
        app_name: str,
        config_id: str,
    ) -> EcrResponse[None]:
        return await self._request(
            "DELETE",
            f"{self.PREFIX}/system/applications/{app_name}/configs/{config_id}",
        )

    async def create_app_version_config(
        self,
        app_version_name: str,
        body: SystemConfigurationInput | Mapping[str, Any],
    ) -> EcrResponse[None]:
        return await self._request(
            "POST",
            f"{self.PREFIX}/system/app-versions/{app_version_name}/configs",
            body=_system_body(body),
        )

    async def list_app_version_configs(
        self,
        app_version_name: str,
    ) -> EcrResponse[SystemConfigurationList]:
        return await self._request(
            "GET",
            f"{self.PREFIX}/system/app-versions/{app_version_name}/configs",
            parser=_system_configurations,
        )

    async def get_current_app_version_config(
        self,
        app_version_name: str,
        *,
        tree_traversal_strategy: Optional[str] = None,
    ) -> EcrResponse[SystemConfiguration]:
        params = _clean({"treeTraversalStrategy": tree_traversal_strategy})
        return await self._request(
            "GET",
            f"{self.PREFIX}/system/app-versions/{app_version_name}/configs/current",
            params=params,
            parser=_system_configuration,
        )

    async def get_app_version_config(
        self,
        app_version_name: str,
        config_id: str,
    ) -> EcrResponse[SystemConfiguration]:
        return await self._request(
            "GET",
            f"{self.PREFIX}/system/app-versions/{app_version_name}/configs/{config_id}",
            parser=_system_configuration,
        )

    async def update_app_version_config(
        self,
        app_version_name: str,
        config_id: str,
        body: SystemConfigurationInput | Mapping[str, Any],
    ) -> EcrResponse[None]:
        return await self._request(
            "PUT",
            f"{self.PREFIX}/system/app-versions/{app_version_name}/configs/{config_id}",
            body=_system_body(body),
        )

    async def delete_app_version_config(
        self,
        app_version_name: str,
        config_id: str,
    ) -> EcrResponse[None]:
        return await self._request(
            "DELETE",
            f"{self.PREFIX}/system/app-versions/{app_version_name}/configs/{config_id}",
        )

    async def create_endpoint_config(
        self,
        endpoint_id: str,
        body: SystemConfigurationInput | Mapping[str, Any],
    ) -> EcrResponse[None]:
        return await self._request(
            "POST",
            f"{self.PREFIX}/system/endpoints/{endpoint_id}/configs",
            body=_system_body(body),
        )

    async def list_endpoint_configs(
        self,
        endpoint_id: str,
    ) -> EcrResponse[SystemConfigurationList]:
        return await self._request(
            "GET",
            f"{self.PREFIX}/system/endpoints/{endpoint_id}/configs",
            parser=_system_configurations,
        )

    async def get_current_endpoint_config(
        self,
        endpoint_id: str,
        *,
        tree_traversal_strategy: Optional[str] = None,
    ) -> EcrResponse[SystemConfiguration]:
        params = _clean({"treeTraversalStrategy": tree_traversal_strategy})
        return await self._request(
            "GET",
            f"{self.PREFIX}/system/endpoints/{endpoint_id}/configs/current",
            params=params,
            parser=_system_configuration,
        )

    async def get_endpoint_config(
        self,
        endpoint_id: str,
        config_id: str,
    ) -> EcrResponse[SystemConfiguration]:
        return await self._request(
            "GET",
            f"{self.PREFIX}/system/endpoints/{endpoint_id}/configs/{config_id}",
            parser=_system_configuration,
        )

    async def update_endpoint_config(
        self,
        endpoint_id: str,
        config_id: str,
        body: SystemConfigurationInput | Mapping[str, Any],
    ) -> EcrResponse[None]:
        return await self._request(
            "PUT",
            f"{self.PREFIX}/system/endpoints/{endpoint_id}/configs/{config_id}",
            body=_system_body(body),
        )

    async def delete_endpoint_config(
        self,
        endpoint_id: str,
        config_id: str,
    ) -> EcrResponse[None]:
        return await self._request(
            "DELETE",
            f"{self.PREFIX}/system/endpoints/{endpoint_id}/configs/{config_id}",
        )
