from __future__ import annotations

import json
import logging
from typing import Any, List

from zmp_zcp_toolkit.wrapper.parameters import (
    GetAlerts,
    GetAlertDetail,
    GetChannels,
    GetIntegrations,
    AlertAction,
    GetPods,
    CreatePod,
    UpdatePod,
    DeletePod,
)
from zmp_zcp_toolkit.wrapper.base_wrapper import BaseAPIWrapper

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


_ALERT_ROOT_PATH = "/api/alert/v1"
_MONITORING_ROOT_PATH = "/api/monitoring/v1"
_MCM_ROOT_PATH = "/api/mcm/resource/v1beta"


class ZcpAnalysisAPIWrapper(BaseAPIWrapper):
    """Wrapper for ZCP Analysis API."""

    @property
    def client(self):
        if not self._client:
            self._client = self._async_client
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    def get_alerts(self, query: GetAlerts) -> List[dict]:
        api_path = f"{_ALERT_ROOT_PATH}/alerts"
        params = query.model_dump(exclude_none=True)
        response = self.client.get(api_path, params=params)
        return response.json()

    def get_priorities(self) -> List[dict]:
        api_path = f"{_ALERT_ROOT_PATH}/alert/priorities"
        response = self.client.get(api_path)
        return response.json()

    def get_severities(self) -> List[dict]:
        api_path = f"{_ALERT_ROOT_PATH}/alert/severities"
        response = self.client.get(api_path)
        return response.json()

    def get_alert_detail(self, query: GetAlertDetail) -> List[dict]:
        api_path = f"{_ALERT_ROOT_PATH}/alerts/{query.alert_id}"
        response = self.client.get(api_path)
        return response.json()

    def get_channels(self, query: GetChannels) -> List[dict]:
        api_path = f"{_ALERT_ROOT_PATH}/channels"
        params = query.model_dump(exclude_none=True)
        response = self.client.get(api_path, params=params)
        return response.json()

    def get_integrations(self, query: GetIntegrations) -> List[dict]:
        api_path = f"{_ALERT_ROOT_PATH}/integrations"
        params = query.model_dump(exclude_none=True)
        response = self.client.get(api_path, params=params)
        return response.json()

    def run(self, mode: str, query: Any) -> str:
        if mode == "get_alerts":
            result = self.get_alerts(query)
            return json.dumps(result)
        elif mode == "get_priorities":
            result = self.get_priorities()
            return json.dumps(result)
        elif mode == "get_severities":
            result = self.get_severities()
            return json.dumps(result)
        elif mode == "get_alert_detail":
            result = self.get_alert_detail(query)
            return json.dumps(result)
        elif mode == "get_channels":
            result = self.get_channels(query)
            return json.dumps(result)
        elif mode == "get_integrations":
            result = self.get_integrations(query)
            return json.dumps(result)
        else:
            raise ValueError(f"Invalid mode: {mode}. The wrapper{__name__} does not support this mode.")


class ZcpSelfHealingAPIWrapper(BaseAPIWrapper):
    """Wrapper for ZCP Self Healing API."""
    
    def alert_action(self, query: AlertAction) -> dict:
        api_path = f"{_ALERT_ROOT_PATH}/alerts/{query.alert_id}/{query.action}"
        params = {}
        if query.snoozed_until_at:
            params["snoozed_until_at"] = query.snoozed_until_at
        response = self.client.patch(api_path, params=params)
        return response.json()

    def get_pods(self, query: GetPods) -> List[dict]:
        api_path = f"{_MCM_ROOT_PATH}/workload/pods"
        params = query.model_dump(exclude_none=True)
        response = self.client.get(api_path, params=params)
        return response.json()

    def create_pod(self, query: CreatePod) -> dict:
        api_path = f"{_MCM_ROOT_PATH}/workload/clusters/{query.cluster}/namespaces/{query.namespace}/pods"
        response = self.client.post(api_path, json=query.body)
        return response.json()

    def update_pod(self, query: UpdatePod) -> dict:
        api_path = f"{_MCM_ROOT_PATH}/workload/clusters/{query.cluster}/namespaces/{query.namespace}/pods/{query.name}"
        response = self.client.put(api_path, json=query.body)
        return response.json()

    def delete_pod(self, query: DeletePod) -> dict:
        api_path = f"{_MCM_ROOT_PATH}/workload/clusters/{query.cluster}/namespaces/{query.namespace}/pods/{query.name}"
        response = self.client.delete(api_path)
        return response.json()

    def run(self, mode: str, query: Any) -> str:
        if mode == "alert_action":
            result = self.alert_action(query)
            return json.dumps(result)
        elif mode == "get_pods":
            result = self.get_pods(query)
            return json.dumps(result)
        elif mode == "create_pod":
            result = self.create_pod(query)
            return json.dumps(result)
        elif mode == "update_pod":
            result = self.update_pod(query)
            return json.dumps(result)
        elif mode == "delete_pod":
            result = self.delete_pod(query)
            return json.dumps(result)
        else:
            raise ValueError(f"Invalid mode: {mode}. The wrapper does not support this mode.")

class ZcpReportAPIWrapper(BaseAPIWrapper):
   ...
