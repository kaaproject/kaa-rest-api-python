# kaa-rest-client

Python client library for [KaaIoT platform](https://www.kaaiot.com/) REST APIs.

## Installation

```bash
pip install kaa-rest-client
```

## Quick Start

```python
import asyncio
from kaa_rest_client import KaaClient, EprClient, EptsClient

async def main():
    async with KaaClient(api_key="your-api-key") as kaa:
        epr = EprClient(kaa)
        endpoints = await epr.list_endpoints(limit=10)
        print(endpoints)

        epts = EptsClient(kaa)
        config = await epts.get_time_series_config()
        print(config)

asyncio.run(main())
```

## Authentication

Two authentication methods are supported:

| Method | Header | Env variable |
|--------|--------|-------------|
| API key (primary) | `x-iamcore-api-key` | `KAA_API_KEY` |
| Bearer token | `Authorization: Bearer ...` | `KAA_BEARER_TOKEN` |

```python
# API key (recommended)
kaa = KaaClient(api_key="your-api-key")

# Bearer token
kaa = KaaClient(bearer_token="your-token")

# Custom base URL
kaa = KaaClient(base_url="https://your-instance.kaaiot.com", api_key="your-api-key")
```

If both are provided, API key takes precedence.

## Service Clients

All service clients use composition — pass a `KaaClient` instance to the constructor.

### EprClient (Endpoint Register)

Manages endpoints, metadata, filters, and relations.

```python
epr = EprClient(kaa)

# List endpoints
endpoints = await epr.list_endpoints(limit=10, sort="endpointId")

# Register a new endpoint
result = await epr.register_endpoint({"endpointId": "my-device", "applicationName": "my-app"})

# Metadata
metadata = await epr.get_endpoint_metadata("endpoint-id")
await epr.update_endpoint_metadata("endpoint-id", {"key": "value"})

# Filters
filters = await epr.list_filters("my-app")
await epr.create_filter("my-app", {"name": "active-devices", "query": "..."})
```

### CexClient (Command Execution)

Invokes commands on endpoints and manages batch operations.

```python
cex = CexClient(kaa)

# Invoke a command
result = await cex.invoke_command("endpoint-id", "reboot", await_timeout=30)

# With payload
result = await cex.invoke_command("endpoint-id", "config", {"brightness": 80})

# Batch command by filter
task = await cex.batch_command_by_filter("reboot", "filter-id")
```

### EptsClient (Endpoint Time Series)

Retrieves time series configuration and data.

```python
epts = EptsClient(kaa)

# Get time series config
config = await epts.get_time_series_config(application_names="my-app")

# Get latest data points
latest = await epts.get_last_time_series("my-app")

# Get historical data
data = await epts.get_time_series_data(
    "my-app",
    time_series_name="temperature",
    from_date="now-7d",
    to_date="now",
)
```

### EcrClient (Endpoint Configuration Registry)

Manages endpoint-delivered configurations, application-version defaults,
configuration schemas/statuses, and platform-side system configurations.

```python
from kaa_rest_client import EcrClient, KaaClient

async with KaaClient(bearer_token="your-token") as kaa:
    ecr = EcrClient(kaa)

    result = await ecr.get_endpoint_configuration("endpoint-id", "app-v1")
    print(result.data.config)
    print(result.etag)
```

Named endpoint-delivered and current system-configuration methods accept an
optional `name`. When omitted, the client sends `name="default"`; pass a
configuration name to address a named configuration.

ECR configuration responses encode the `config` field as a JSON string. The
client parses valid JSON strings into dictionaries, lists, scalar values, or
`None`; malformed JSON remains the original string. Endpoint configuration
requests are sent as raw JSON bodies.

System configurations can use a DTO, which serializes structured configuration
values into the API's string field:

```python
from kaa_rest_client import SystemConfigurationInput

body = SystemConfigurationInput(
    name="alert-email-recipients",
    display_name="Alert email recipients",
    config={"emails": ["alert-monitor@acme.com"]},
)

async with KaaClient(bearer_token="your-token") as kaa:
    ecr = EcrClient(kaa)
    await ecr.create_application_config("my-app", body)
    current = await ecr.get_current_application_config("my-app")
    print(current.data.config)
```

System configuration (`/system/...`) is primarily for static defaults or
platform-side static configuration. Updating it does not directly ship the
configuration to devices over MQTT. Use endpoint/application-version
configuration methods for device-delivered configuration. ECR methods return
an `EcrResponse` containing `data`, `status_code`, and response headers such as
`ETag` and `Location`.

### AsfClient (Analytics Security Facade)

Manages ingest pipelines, index templates, and searches documents.

```python
asf = AsfClient(kaa)

# Ingest pipelines
await asf.upsert_pipeline("my-pipeline", {"processors": [...]})
pipeline = await asf.get_pipeline("my-pipeline")

# Search documents
results = await asf.search_documents("tenant-id", "my-app", "2024.01.15", {
    "query": {"match_all": {}}
})
```

### ReClient (Rule Engine)

Manages rules, actions, triggers, alerts, alert settings, and rule execution.

```python
re = ReClient(kaa)

# Rules
rules = await re.list_rules()
rule = await re.get_rule("rule-id")
await re.execute_rule("rule-id")

# Alerts
alerts = await re.list_alerts(entity_type="endpoint", state="OPEN")
```

### TektonClient (Application and Configuration Management)

Manages service instances, applications, application versions, application and
tenant configurations, and bulk configuration exports.

```python
tekton = TektonClient(kaa)

applications = await tekton.list_applications()
versions = await tekton.list_app_versions("my-app")
config = await tekton.get_app_config("my-app")
export = await tekton.bulk_export()
```

### AmClient (Asset Management)

Manages asset types, assets, and relations between platform entities.

```python
am = AmClient(kaa)

asset_types = await am.list_asset_types()
assets = await am.list_assets()
relations = await am.get_relations("entity-id")
```

### TenantManagerClient (Tenant Manager)

Manages tenants, tenant credentials, package types, subscriptions, and user
templates.

```python
tenant_manager = TenantManagerClient(kaa)

tenants = await tenant_manager.list_tenants(limit=10)
tenant = await tenant_manager.get_tenant("tenant-id")
credentials = await tenant_manager.get_tenant_credentials("tenant-id")
subscriptions = await tenant_manager.list_subscriptions("tenant-id")
```

## Connection Pooling

You can pass an external `httpx.AsyncClient` to share connection pools:

```python
import httpx

async with httpx.AsyncClient() as http:
    kaa = KaaClient(api_key="key", client=http)
    epr = EprClient(kaa)
    # ...
```

## Error Handling

```python
from kaa_rest_client import KaaApiError, KaaAuthError, KaaNotFoundError

try:
    endpoint = await epr.get_endpoint("nonexistent")
except KaaNotFoundError:
    print("Endpoint not found")
except KaaAuthError:
    print("Authentication failed")
except KaaApiError as e:
    print(f"API error {e.status_code}: {e.message}")
```
