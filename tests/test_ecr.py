import json
import unittest

import httpx

from kaa_rest_client.client import KaaClient
from kaa_rest_client.ecr import EcrClient
from kaa_rest_client.ecr_models import (
    EndpointConfiguration,
    SystemConfiguration,
    SystemConfigurationInput,
)


ENDPOINT_CONFIGURATION = {
    "configId": "231f1aae-a4be-11ea-bb37-0242ac130002",
    "name": "night-mode",
    "config": '{"active": true, "pushInterval": 5}',
    "createdDate": "2017-03-17T11:30:02.643Z",
    "updatedDate": "2017-03-17T11:30:02.643Z",
}

SYSTEM_CONFIGURATION = {
    "configId": "89449e85-7721-4437-8f25-23a99fe45a1c",
    "name": "alert-email-recipients",
    "displayName": "Alert email recipients",
    "config": '{"emails": ["alert-monitor@acme.com"]}',
    "createdAt": "2024-02-02T01:23:29.841Z",
    "updatedAt": "2024-02-02T01:23:29.841Z",
}


class EcrEndpointRouteTests(unittest.IsolatedAsyncioTestCase):
    async def test_named_endpoint_configuration_defaults_and_overrides_name(self):
        seen = []

        def handler(request: httpx.Request) -> httpx.Response:
            seen.append(request)
            return httpx.Response(
                200,
                json=ENDPOINT_CONFIGURATION,
                request=request,
            )

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            ecr = EcrClient(KaaClient(base_url="https://example.test", client=http))

            await ecr.get_endpoint_configuration("e1", "app-v1")
            self.assertEqual(dict(seen[-1].url.params), {"name": "default"})

            await ecr.get_endpoint_configuration(
                "e1", "app-v1", name="night-mode",
            )
            self.assertEqual(dict(seen[-1].url.params), {"name": "night-mode"})

            await ecr.upsert_endpoint_configuration(
                "e1", "app-v1", {"active": True}, name="night-mode",
            )
            self.assertEqual(dict(seen[-1].url.params), {"name": "night-mode"})

            await ecr.delete_endpoint_configuration(
                "e1", "app-v1", name="night-mode",
            )
            self.assertEqual(dict(seen[-1].url.params), {"name": "night-mode"})

            await ecr.get_app_version_configuration("app-v1")
            self.assertEqual(dict(seen[-1].url.params), {"name": "default"})

            await ecr.get_app_version_configuration(
                "app-v1", name="night-mode",
            )
            self.assertEqual(dict(seen[-1].url.params), {"name": "night-mode"})

    async def test_endpoint_and_app_version_routes(self):
        seen = []

        def handler(request: httpx.Request) -> httpx.Response:
            seen.append(request)
            path = request.url.path
            if path.endswith("/configurations"):
                body = [ENDPOINT_CONFIGURATION]
            elif path.endswith("/schemas"):
                body = {"type": "object"}
            elif request.method == "DELETE":
                return httpx.Response(204, request=request)
            elif path.endswith("/statuses"):
                body = {"content": [], "totalElements": 0}
            elif "/batch" in path or "/filters/" in path or path.endswith("/validate"):
                return httpx.Response(200, request=request)
            else:
                body = ENDPOINT_CONFIGURATION
            return httpx.Response(
                200,
                headers={"ETag": "endpoint-etag"},
                json=body,
                request=request,
            )

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            ecr = EcrClient(KaaClient(base_url="https://example.test", client=http))
            cases = [
                (
                    lambda: ecr.upsert_endpoint_configuration(
                        "e1", "app-v1", {"active": True},
                    ),
                    "PUT",
                    "/ecr/api/v1/endpoints/e1/app-versions/app-v1",
                    {"active": True},
                ),
                (
                    lambda: ecr.get_endpoint_configuration("e1", "app-v1"),
                    "GET",
                    "/ecr/api/v1/endpoints/e1/app-versions/app-v1",
                    None,
                ),
                (
                    lambda: ecr.delete_endpoint_configuration("e1", "app-v1"),
                    "DELETE",
                    "/ecr/api/v1/endpoints/e1/app-versions/app-v1",
                    None,
                ),
                (
                    lambda: ecr.list_endpoint_configurations("e1", "app-v1"),
                    "GET",
                    "/ecr/api/v1/endpoints/e1/app-versions/app-v1/configurations",
                    None,
                ),
                (
                    lambda: ecr.bulk_upsert_endpoint_configurations(
                        {"configPayload": {}, "endpoints": {}},
                    ),
                    "PUT",
                    "/ecr/api/v1/endpoints/batch",
                    {"configPayload": {}, "endpoints": {}},
                ),
                (
                    lambda: ecr.upsert_endpoint_configurations_by_filter(
                        "filter-1", {"active": True},
                    ),
                    "PUT",
                    "/ecr/api/v1/endpoints/filters/filter-1",
                    {"active": True},
                ),
                (
                    lambda: ecr.upsert_app_version_configuration(
                        "app-v1", {"active": True},
                    ),
                    "PUT",
                    "/ecr/api/v1/app-versions/app-v1",
                    {"active": True},
                ),
                (
                    lambda: ecr.get_app_version_configuration("app-v1"),
                    "GET",
                    "/ecr/api/v1/app-versions/app-v1",
                    None,
                ),
                (
                    lambda: ecr.delete_app_version_configuration("app-v1"),
                    "DELETE",
                    "/ecr/api/v1/app-versions/app-v1",
                    None,
                ),
                (
                    lambda: ecr.list_app_version_configurations("app-v1"),
                    "GET",
                    "/ecr/api/v1/app-versions/app-v1/configurations",
                    None,
                ),
                (
                    lambda: ecr.get_app_version_schema("app-v1"),
                    "GET",
                    "/ecr/api/v1/app-versions/app-v1/schemas",
                    None,
                ),
                (
                    lambda: ecr.validate_app_version_schema(
                        "app-v1", {"type": "object"},
                    ),
                    "PUT",
                    "/ecr/api/v1/app-versions/app-v1/schemas/validate",
                    {"type": "object"},
                ),
            ]

            for call, method, path, body in cases:
                seen.clear()
                result = await call()
                request = seen[-1]
                self.assertEqual(request.method, method)
                self.assertEqual(request.url.path, path)
                if body is None:
                    self.assertEqual(request.content, b"")
                else:
                    self.assertEqual(json.loads(request.content), body)
                if method in {"GET", "PUT"} and path.endswith("app-v1"):
                    self.assertIsInstance(result.data, EndpointConfiguration)
                    self.assertEqual(result.etag, "endpoint-etag")

    async def test_status_route_uses_optional_query_parameters(self):
        seen = []

        def handler(request: httpx.Request) -> httpx.Response:
            seen.append(request)
            return httpx.Response(
                200,
                json={"content": [], "totalElements": 0},
                request=request,
            )

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            ecr = EcrClient(KaaClient(base_url="https://example.test", client=http))
            result = await ecr.list_configuration_statuses(
                "e1", app_version_name="app-v1", config_id="config-1",
            )

        self.assertEqual(result.data.content, [])
        self.assertEqual(
            dict(seen[0].url.params),
            {
                "endpointId": "e1",
                "appVersionName": "app-v1",
                "configId": "config-1",
            },
        )


class EcrTenantApplicationRouteTests(unittest.IsolatedAsyncioTestCase):
    async def test_tenant_and_application_system_routes(self):
        seen = []

        def handler(request: httpx.Request) -> httpx.Response:
            seen.append(request)
            path = request.url.path
            if request.method == "POST":
                return httpx.Response(
                    201,
                    headers={
                        "ETag": "system-etag",
                        "Location": "/ecr/api/v1/system/configs/1",
                    },
                    request=request,
                )
            if request.method in {"PUT", "DELETE"}:
                return httpx.Response(204, request=request)
            if path.endswith("/configs"):
                return httpx.Response(
                    200,
                    json={"content": [SYSTEM_CONFIGURATION], "totalElements": 1},
                    request=request,
                )
            return httpx.Response(200, json=SYSTEM_CONFIGURATION, request=request)

        body = SystemConfigurationInput(
            name="alert-email-recipients",
            display_name="Alert email recipients",
            config={"emails": ["alert-monitor@acme.com"]},
        )

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            ecr = EcrClient(KaaClient(base_url="https://example.test", client=http))
            cases = [
                (
                    lambda: ecr.create_tenant_config("tenant-1", body),
                    "POST",
                    "/ecr/api/v1/system/tenants/tenant-1/configs",
                    True,
                ),
                (
                    lambda: ecr.list_tenant_configs("tenant-1"),
                    "GET",
                    "/ecr/api/v1/system/tenants/tenant-1/configs",
                    False,
                ),
                (
                    lambda: ecr.get_current_tenant_config("tenant-1"),
                    "GET",
                    "/ecr/api/v1/system/tenants/tenant-1/configs/current",
                    False,
                ),
                (
                    lambda: ecr.get_tenant_config("tenant-1", "config-1"),
                    "GET",
                    "/ecr/api/v1/system/tenants/tenant-1/configs/config-1",
                    False,
                ),
                (
                    lambda: ecr.update_tenant_config("tenant-1", "config-1", body),
                    "PUT",
                    "/ecr/api/v1/system/tenants/tenant-1/configs/config-1",
                    True,
                ),
                (
                    lambda: ecr.delete_tenant_config("tenant-1", "config-1"),
                    "DELETE",
                    "/ecr/api/v1/system/tenants/tenant-1/configs/config-1",
                    False,
                ),
                (
                    lambda: ecr.create_application_config("app-1", body),
                    "POST",
                    "/ecr/api/v1/system/applications/app-1/configs",
                    True,
                ),
                (
                    lambda: ecr.list_application_configs("app-1"),
                    "GET",
                    "/ecr/api/v1/system/applications/app-1/configs",
                    False,
                ),
                (
                    lambda: ecr.get_current_application_config(
                        "app-1",
                        name="alert-email-recipients",
                        tree_traversal_strategy="SKIP",
                    ),
                    "GET",
                    "/ecr/api/v1/system/applications/app-1/configs/current",
                    False,
                ),
                (
                    lambda: ecr.get_application_config("app-1", "config-1"),
                    "GET",
                    "/ecr/api/v1/system/applications/app-1/configs/config-1",
                    False,
                ),
                (
                    lambda: ecr.update_application_config("app-1", "config-1", body),
                    "PUT",
                    "/ecr/api/v1/system/applications/app-1/configs/config-1",
                    True,
                ),
                (
                    lambda: ecr.delete_application_config("app-1", "config-1"),
                    "DELETE",
                    "/ecr/api/v1/system/applications/app-1/configs/config-1",
                    False,
                ),
            ]

            for call, method, path, has_body in cases:
                seen.clear()
                result = await call()
                request = seen[-1]
                self.assertEqual(request.method, method)
                self.assertEqual(request.url.path, path)
                if has_body:
                    self.assertEqual(
                        json.loads(request.content),
                        {
                            "name": "alert-email-recipients",
                            "displayName": "Alert email recipients",
                            "config": '{"emails": ["alert-monitor@acme.com"]}',
                        },
                    )
                if method == "POST":
                    self.assertIsNone(result.data)
                    self.assertEqual(result.etag, "system-etag")
                    self.assertEqual(result.location, "/ecr/api/v1/system/configs/1")
                elif method == "GET" and path.endswith("/configs"):
                    self.assertEqual(result.data.total_elements, 1)
                    self.assertIsInstance(result.data.content[0], SystemConfiguration)
                elif method == "GET":
                    self.assertIsInstance(result.data, SystemConfiguration)
                    self.assertEqual(
                        result.data.config,
                        {"emails": ["alert-monitor@acme.com"]},
                    )

                if path.endswith("/applications/app-1/configs/current"):
                    self.assertEqual(
                        dict(request.url.params),
                        {
                            "name": "alert-email-recipients",
                            "treeTraversalStrategy": "SKIP",
                        },
                    )
                if path.endswith("/tenants/tenant-1/configs/current"):
                    self.assertEqual(
                        dict(request.url.params),
                        {"name": "default"},
                    )


class EcrAppVersionEndpointSystemRouteTests(unittest.IsolatedAsyncioTestCase):
    async def test_app_version_and_endpoint_system_routes(self):
        seen = []

        def handler(request: httpx.Request) -> httpx.Response:
            seen.append(request)
            path = request.url.path
            if request.method == "POST":
                return httpx.Response(201, request=request)
            if request.method in {"PUT", "DELETE"}:
                return httpx.Response(204, request=request)
            if path.endswith("/configs"):
                return httpx.Response(
                    200,
                    json={"content": [SYSTEM_CONFIGURATION], "totalElements": 1},
                    request=request,
                )
            return httpx.Response(200, json=SYSTEM_CONFIGURATION, request=request)

        body = SystemConfigurationInput(
            name="alert-email-recipients",
            config={"emails": ["alert-monitor@acme.com"]},
        )

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            ecr = EcrClient(KaaClient(base_url="https://example.test", client=http))
            cases = [
                (
                    lambda: ecr.create_app_version_config("app-v1", body),
                    "POST",
                    "/ecr/api/v1/system/app-versions/app-v1/configs",
                ),
                (
                    lambda: ecr.list_app_version_configs("app-v1"),
                    "GET",
                    "/ecr/api/v1/system/app-versions/app-v1/configs",
                ),
                (
                    lambda: ecr.get_current_app_version_config(
                        "app-v1",
                        name="alert-email-recipients",
                        tree_traversal_strategy="SKIP",
                    ),
                    "GET",
                    "/ecr/api/v1/system/app-versions/app-v1/configs/current",
                ),
                (
                    lambda: ecr.get_app_version_config("app-v1", "config-1"),
                    "GET",
                    "/ecr/api/v1/system/app-versions/app-v1/configs/config-1",
                ),
                (
                    lambda: ecr.update_app_version_config("app-v1", "config-1", body),
                    "PUT",
                    "/ecr/api/v1/system/app-versions/app-v1/configs/config-1",
                ),
                (
                    lambda: ecr.delete_app_version_config("app-v1", "config-1"),
                    "DELETE",
                    "/ecr/api/v1/system/app-versions/app-v1/configs/config-1",
                ),
                (
                    lambda: ecr.create_endpoint_config("e1", body),
                    "POST",
                    "/ecr/api/v1/system/endpoints/e1/configs",
                ),
                (
                    lambda: ecr.list_endpoint_configs("e1"),
                    "GET",
                    "/ecr/api/v1/system/endpoints/e1/configs",
                ),
                (
                    lambda: ecr.get_current_endpoint_config(
                        "e1",
                        name="alert-email-recipients",
                        tree_traversal_strategy="SKIP",
                    ),
                    "GET",
                    "/ecr/api/v1/system/endpoints/e1/configs/current",
                ),
                (
                    lambda: ecr.get_endpoint_config("e1", "config-1"),
                    "GET",
                    "/ecr/api/v1/system/endpoints/e1/configs/config-1",
                ),
                (
                    lambda: ecr.update_endpoint_config("e1", "config-1", body),
                    "PUT",
                    "/ecr/api/v1/system/endpoints/e1/configs/config-1",
                ),
                (
                    lambda: ecr.delete_endpoint_config("e1", "config-1"),
                    "DELETE",
                    "/ecr/api/v1/system/endpoints/e1/configs/config-1",
                ),
            ]

            for call, method, path in cases:
                seen.clear()
                result = await call()
                request = seen[-1]
                self.assertEqual(request.method, method)
                self.assertEqual(request.url.path, path)
                if method == "GET" and path.endswith("/configs"):
                    self.assertEqual(result.data.total_elements, 1)
                elif method == "GET":
                    self.assertIsInstance(result.data, SystemConfiguration)
                if path.endswith("/configs/current"):
                    if path.endswith("/app-versions/app-v1/configs/current"):
                        expected_params = {
                            "name": "alert-email-recipients",
                            "treeTraversalStrategy": "SKIP",
                        }
                    elif path.endswith("/endpoints/e1/configs/current"):
                        expected_params = {
                            "name": "alert-email-recipients",
                            "treeTraversalStrategy": "SKIP",
                        }
                    else:
                        expected_params = {"name": "default"}
                    self.assertEqual(dict(request.url.params), expected_params)


class EcrExportsTests(unittest.TestCase):
    def test_ecr_public_types_are_exported(self):
        from kaa_rest_client import (
            EcrClient,
            EcrResponse,
            EndpointConfiguration,
            SystemConfiguration,
            SystemConfigurationInput,
        )

        self.assertIsNotNone(EcrClient)
        self.assertIsNotNone(EcrResponse)
        self.assertIsNotNone(EndpointConfiguration)
        self.assertIsNotNone(SystemConfiguration)
        self.assertIsNotNone(SystemConfigurationInput)


if __name__ == "__main__":
    unittest.main()
