from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, Generic, List, Mapping, Optional, TypeVar, Union


JsonValue = Union[Dict[str, Any], List[Any], str, int, float, bool, None]


def parse_config(value: object) -> JsonValue:
    """Decode a JSON-encoded configuration value without hiding malformed input."""
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _serialize_config(value: JsonValue) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value)


@dataclass(frozen=True)
class EndpointConfiguration:
    config_id: str
    name: str
    config: JsonValue
    created_date: str
    updated_date: str

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "EndpointConfiguration":
        return cls(
            config_id=payload["configId"],
            name=payload["name"],
            config=parse_config(payload.get("config")),
            created_date=payload["createdDate"],
            updated_date=payload["updatedDate"],
        )


@dataclass(frozen=True)
class SystemConfiguration:
    config_id: str
    name: str
    display_name: Optional[str]
    config: JsonValue
    created_at: str
    updated_at: str

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "SystemConfiguration":
        return cls(
            config_id=payload["configId"],
            name=payload["name"],
            display_name=payload.get("displayName"),
            config=parse_config(payload.get("config")),
            created_at=payload["createdAt"],
            updated_at=payload["updatedAt"],
        )


@dataclass(frozen=True)
class SystemConfigurationInput:
    name: str
    config: JsonValue
    display_name: Optional[str] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "name": self.name,
            "config": _serialize_config(self.config),
        }
        if self.display_name is not None:
            payload["displayName"] = self.display_name
        return payload


@dataclass(frozen=True)
class SystemConfigurationList:
    content: List[SystemConfiguration]
    total_elements: int

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "SystemConfigurationList":
        content = [
            SystemConfiguration.from_dict(item)
            for item in payload.get("content", [])
        ]
        return cls(
            content=content,
            total_elements=payload.get("totalElements", len(content)),
        )


@dataclass(frozen=True)
class ConfigurationStatus:
    config_id: str
    endpoint_id: str
    app_version_name: str
    status: str
    config: Optional[JsonValue] = None
    last_dispatched_date: Optional[str] = None
    last_confirmed_date: Optional[str] = None
    confirmation_status_code: Optional[int] = None
    confirmation_reason_phrase: Optional[Union[str, int]] = None

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ConfigurationStatus":
        return cls(
            config_id=payload["configId"],
            endpoint_id=payload["endpointId"],
            app_version_name=payload["appVersionName"],
            status=payload["status"],
            config=parse_config(payload.get("config")),
            last_dispatched_date=payload.get("lastDispatchedDate"),
            last_confirmed_date=payload.get("lastConfirmedDate"),
            confirmation_status_code=payload.get("confirmationStatusCode"),
            confirmation_reason_phrase=payload.get("confirmationReasonPhrase"),
        )


@dataclass(frozen=True)
class ConfigurationStatusPage:
    content: List[ConfigurationStatus] = field(default_factory=list)
    pageable: Dict[str, Any] = field(default_factory=dict)
    total_elements: int = 0
    total_pages: int = 0
    last: bool = False
    sort: Dict[str, Any] = field(default_factory=dict)
    number_of_elements: int = 0
    first: bool = False
    size: int = 0
    number: int = 0
    empty: bool = True

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ConfigurationStatusPage":
        return cls(
            content=[
                ConfigurationStatus.from_dict(item)
                for item in payload.get("content", [])
            ],
            pageable=dict(payload.get("pageable", {})),
            total_elements=payload.get("totalElements", 0),
            total_pages=payload.get("totalPages", 0),
            last=payload.get("last", False),
            sort=dict(payload.get("sort", {})),
            number_of_elements=payload.get("numberOfElements", 0),
            first=payload.get("first", False),
            size=payload.get("size", 0),
            number=payload.get("number", 0),
            empty=payload.get("empty", True),
        )


@dataclass(frozen=True)
class BulkConfigurationRequest:
    config_payload: JsonValue
    endpoints: Dict[str, List[str]]

    def to_payload(self) -> Dict[str, Any]:
        return {
            "configPayload": self.config_payload,
            "endpoints": self.endpoints,
        }


T = TypeVar("T")


@dataclass(frozen=True)
class EcrResponse(Generic[T]):
    data: Optional[T]
    status_code: int
    headers: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        normalized = {
            str(name).lower(): str(value)
            for name, value in self.headers.items()
        }
        object.__setattr__(self, "headers", normalized)

    @property
    def etag(self) -> Optional[str]:
        return self.headers.get("etag")

    @property
    def location(self) -> Optional[str]:
        return self.headers.get("location")
