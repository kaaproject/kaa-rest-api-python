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
