from __future__ import annotations

from typing import Any

from .client import KaaClient


def _clean(d: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in d.items() if v is not None}


class ReClient:
    PREFIX = "/re/api/v1"

    def __init__(self, c: KaaClient):
        self._c = c

    # ------------------------------------------------------------------
    # Rules
    # ------------------------------------------------------------------

    # 1. POST /rules
    async def create_rule(self, body: dict[str, Any]) -> Any:
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/rules",
            json=body,
        )

    # 2. GET /rules
    async def list_rules(self) -> Any:
        return await self._c.request("GET", f"{self.PREFIX}/rules")

    # 3. GET /rules/{ruleId}
    async def get_rule(self, rule_id: str) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/rules/{rule_id}",
        )

    # 4. PUT /rules/{ruleId}
    async def update_rule(
        self,
        rule_id: str,
        body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/rules/{rule_id}",
            json=body,
        )

    # 5. DELETE /rules/{ruleId}
    async def delete_rule(self, rule_id: str) -> Any:
        return await self._c.request(
            "DELETE",
            f"{self.PREFIX}/rules/{rule_id}",
        )

    # 6. POST /rules/{ruleId}/execute
    async def execute_rule(
        self,
        rule_id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/rules/{rule_id}/execute",
            json=body,
        )

    # 7. GET /rules/{ruleId}/actions
    async def get_rule_actions(self, rule_id: str) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/rules/{rule_id}/actions",
        )

    # 8. GET /rules/{ruleId}/triggers
    async def get_rule_triggers(self, rule_id: str) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/rules/{rule_id}/triggers",
        )

    # ------------------------------------------------------------------
    # Attached actions/triggers per rule
    # ------------------------------------------------------------------

    # 9. PUT /rules/{ruleId}/action-types/{actionType}/actions
    async def update_rule_actions(
        self,
        rule_id: str,
        action_type: str,
        body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/rules/{rule_id}/action-types/{action_type}/actions",
            json=body,
        )

    # 10. PUT /rules/{ruleId}/trigger-types/{triggerType}/triggers
    async def update_rule_triggers(
        self,
        rule_id: str,
        trigger_type: str,
        body: Any,
    ) -> Any:
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/rules/{rule_id}/trigger-types/{trigger_type}/triggers",
            json=body,
        )

    # 11. PATCH /rules/{ruleId}/trigger-types/cron/triggers
    async def patch_rule_cron_triggers(
        self,
        rule_id: str,
        body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "PATCH",
            f"{self.PREFIX}/rules/{rule_id}/trigger-types/cron/triggers",
            json=body,
        )

    # ------------------------------------------------------------------
    # Action CRUD (generic for all 9 action types)
    # ------------------------------------------------------------------

    # 12. POST /action-types/{actionType}/actions
    async def create_action(
        self,
        action_type: str,
        body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/action-types/{action_type}/actions",
            json=body,
        )

    # 13. GET /action-types/{actionType}/actions
    async def list_actions(
        self,
        action_type: str,
        *,
        rule_id: str | None = None,
    ) -> Any:
        params = _clean({"ruleId": rule_id})
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/action-types/{action_type}/actions",
            params=params or None,
        )

    # 14. GET /action-types/{actionType}/actions/{actionId}
    async def get_action(
        self,
        action_type: str,
        action_id: str,
    ) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/action-types/{action_type}/actions/{action_id}",
        )

    # 15. PUT /action-types/{actionType}/actions/{actionId}
    async def update_action(
        self,
        action_type: str,
        action_id: str,
        body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/action-types/{action_type}/actions/{action_id}",
            json=body,
        )

    # 16. DELETE /action-types/{actionType}/actions/{actionId}
    async def delete_action(
        self,
        action_type: str,
        action_id: str,
    ) -> Any:
        return await self._c.request(
            "DELETE",
            f"{self.PREFIX}/action-types/{action_type}/actions/{action_id}",
        )

    # ------------------------------------------------------------------
    # Trigger CRUD (generic for all 8 trigger types)
    # ------------------------------------------------------------------

    # 17. POST /trigger-types/{triggerType}/triggers
    async def create_trigger(
        self,
        trigger_type: str,
        body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/trigger-types/{trigger_type}/triggers",
            json=body,
        )

    # 18. GET /trigger-types/{triggerType}/triggers
    async def list_triggers(self, trigger_type: str) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/trigger-types/{trigger_type}/triggers",
        )

    # 19. GET /trigger-types/{triggerType}/triggers/{triggerId}
    async def get_trigger(
        self,
        trigger_type: str,
        trigger_id: str,
    ) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/trigger-types/{trigger_type}/triggers/{trigger_id}",
        )

    # 20. PUT /trigger-types/{triggerType}/triggers/{triggerId}
    async def update_trigger(
        self,
        trigger_type: str,
        trigger_id: str,
        body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/trigger-types/{trigger_type}/triggers/{trigger_id}",
            json=body,
        )

    # 21. DELETE /trigger-types/{triggerType}/triggers/{triggerId}
    async def delete_trigger(
        self,
        trigger_type: str,
        trigger_id: str,
    ) -> Any:
        return await self._c.request(
            "DELETE",
            f"{self.PREFIX}/trigger-types/{trigger_type}/triggers/{trigger_id}",
        )

    # ------------------------------------------------------------------
    # Alerts (instances)
    # ------------------------------------------------------------------

    # 22. GET /alerts
    async def list_alerts(
        self,
        entity_type: str,
        *,
        entity_ids: str | None = None,
        alert_setting_id: str | None = None,
        alert_type: str | None = None,
        state: str | None = None,
        acknowledgement: str | None = None,
        severity_level: str | None = None,
        entity_metadata_path: str | None = None,
        entity_metadata_value: str | None = None,
        metadata_path: str | None = None,
        metadata_value: str | None = None,
        from_started_at: str | None = None,
        to_started_at: str | None = None,
        sort: str | None = None,
        sort_order: str | None = None,
    ) -> Any:
        params = _clean(
            {
                "entityType": entity_type,
                "entityIds": entity_ids,
                "alertSettingId": alert_setting_id,
                "alertType": alert_type,
                "state": state,
                "acknowledgement": acknowledgement,
                "severityLevel": severity_level,
                "entityMetadataPath": entity_metadata_path,
                "entityMetadataValue": entity_metadata_value,
                "metadataPath": metadata_path,
                "metadataValue": metadata_value,
                "fromStartedAt": from_started_at,
                "toStartedAt": to_started_at,
                "sort": sort,
                "sortOrder": sort_order,
            }
        )
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/alerts",
            params=params,
        )

    # 23. POST /alerts/search
    async def search_alerts(self, body: dict[str, Any]) -> Any:
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/alerts/search",
            json=body,
        )

    # 24. POST /alerts/delete
    async def bulk_delete_alerts(self, body: dict[str, Any]) -> Any:
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/alerts/delete",
            json=body,
        )

    # 25. DELETE /alerts/{alertId}
    async def delete_alert(
        self,
        alert_id: str,
        entity_id: str,
        entity_type: str,
    ) -> Any:
        return await self._c.request(
            "DELETE",
            f"{self.PREFIX}/alerts/{alert_id}",
            params={"entityId": entity_id, "entityType": entity_type},
        )

    # 26. GET /alerts/types
    async def list_alert_types(self, entity_type: str) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/alerts/types",
            params={"entityType": entity_type},
        )

    # 27. GET /alerts/metadata-keys
    async def get_alert_metadata_keys(
        self,
        metadata_keys_type: str,
    ) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/alerts/metadata-keys",
            params={"metadataKeysType": metadata_keys_type},
        )

    # 28. PUT /alerts/{alertId}/acknowledgement
    async def acknowledge_alert(
        self,
        alert_id: str,
        entity_id: str,
        entity_type: str,
        body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/alerts/{alert_id}/acknowledgement",
            params={"entityId": entity_id, "entityType": entity_type},
            json=body,
        )

    # 29. PUT /alerts/{alertId}/resolve
    async def resolve_alert(
        self,
        alert_id: str,
        body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/alerts/{alert_id}/resolve",
            json=body,
        )

    # 30. GET /alerts/{alertId}/lifecycle-events
    async def get_alert_lifecycle_events(
        self,
        alert_id: str,
        entity_id: str,
        entity_type: str,
        *,
        event_type: str | None = None,
        sort: str | None = None,
        sort_order: str | None = None,
    ) -> Any:
        params = _clean(
            {
                "entityId": entity_id,
                "entityType": entity_type,
                "eventType": event_type,
                "sort": sort,
                "sortOrder": sort_order,
            }
        )
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/alerts/{alert_id}/lifecycle-events",
            params=params,
        )

    # ------------------------------------------------------------------
    # Alert settings
    # ------------------------------------------------------------------

    # 31. POST /alert-settings
    async def create_alert_setting(self, body: dict[str, Any]) -> Any:
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/alert-settings",
            json=body,
        )

    # 32. GET /alert-settings
    async def list_alert_settings(self) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/alert-settings",
        )

    # 33. GET /alert-settings/{alertSettingId}
    async def get_alert_setting(self, alert_setting_id: str) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/alert-settings/{alert_setting_id}",
        )

    # 34. PUT /alert-settings/{alertSettingId}
    async def update_alert_setting(
        self,
        alert_setting_id: str,
        body: dict[str, Any],
    ) -> Any:
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/alert-settings/{alert_setting_id}",
            json=body,
        )

    # 35. DELETE /alert-settings/{alertSettingId}
    async def delete_alert_setting(self, alert_setting_id: str) -> Any:
        return await self._c.request(
            "DELETE",
            f"{self.PREFIX}/alert-settings/{alert_setting_id}",
        )

    # ------------------------------------------------------------------
    # Snippets
    # ------------------------------------------------------------------

    # 36. POST /snippets
    async def create_snippet(self, body: dict[str, Any]) -> Any:
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/snippets",
            json=body,
        )

    # 37. GET /snippets
    async def list_snippets(self) -> Any:
        return await self._c.request("GET", f"{self.PREFIX}/snippets")

    # 38. GET /snippets/{snippetId}
    async def get_snippet(self, snippet_id: str) -> Any:
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/snippets/{snippet_id}",
        )

    # 39. PUT /snippets/{snippetId}
    async def update_snippet(self, snippet_id: str, body: dict[str, Any]) -> Any:
        return await self._c.request(
            "PUT",
            f"{self.PREFIX}/snippets/{snippet_id}",
            json=body,
        )

    # 40. DELETE /snippets/{snippetId}
    async def delete_snippet(self, snippet_id: str) -> Any:
        return await self._c.request(
            "DELETE",
            f"{self.PREFIX}/snippets/{snippet_id}",
        )

    # ------------------------------------------------------------------
    # Traces
    # ------------------------------------------------------------------

    async def list_traces(
        self,
        *,
        trace_id: str | None = None,
        entity_type: str | None = None,
        entity_id: str | None = None,
        raised_on_entity_type: str | None = None,
        raised_on_entity_id: str | None = None,
        outcome: str | None = None,
        from_created_at: str | None = None,
        to_created_at: str | None = None,
        include: str | None = None,
    ) -> Any:
        params = _clean(
            {
                "traceId": trace_id,
                "entityType": entity_type,
                "entityId": entity_id,
                "raisedOnEntityType": raised_on_entity_type,
                "raisedOnEntityId": raised_on_entity_id,
                "outcome": outcome,
                "fromCreatedAt": from_created_at,
                "toCreatedAt": to_created_at,
                "include": include,
            }
        )
        return await self._c.request(
            "GET",
            f"{self.PREFIX}/traces",
            params=params,
        )

    async def delete_traces(
        self,
        *,
        before_date: str | None = None,
    ) -> Any:
        params = _clean({"beforeDate": before_date})
        return await self._c.request(
            "DELETE",
            f"{self.PREFIX}/traces",
            params=params,
        )

    # ------------------------------------------------------------------
    # Expression evaluation
    # ------------------------------------------------------------------

    # 41. POST /expressions/evaluation
    async def evaluate_expression(self, body: dict[str, Any]) -> Any:
        return await self._c.request(
            "POST",
            f"{self.PREFIX}/expressions/evaluation",
            json=body,
        )
