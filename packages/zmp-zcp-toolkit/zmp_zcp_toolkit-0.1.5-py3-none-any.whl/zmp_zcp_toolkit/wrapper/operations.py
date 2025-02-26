from typing import Dict, List

from zmp_zcp_toolkit.wrapper.api_wrapper import (
    ZcpAnalysisAPIWrapper,
    ZcpSelfHealingAPIWrapper,
    ZcpReportAPIWrapper,
)
from zmp_zcp_toolkit.wrapper.base_wrapper import BaseAPIWrapper
from zmp_zcp_toolkit.wrapper.parameters import (
    AlertAction,
    CreatePod,
    DeletePod,
    GetAlertDetail,
    GetAlerts,
    GetChannels,
    GetIntegrations,
    GetPods,
    NoInput,
    UpdatePod,
)
from zmp_zcp_toolkit.wrapper.prompts import (
    ALERT_ACTION_PROMPT,
    CREATE_POD_PROMPT,
    DELETE_POD_PROMPT,
    GET_ALERT_DETAIL_PROMPT,
    GET_ALERTS_PROMPT,
    GET_CHANNELS_PROMPT,
    GET_INTEGRATIONS_PROMPT,
    GET_PODS_PROMPT,
    GET_PRIORITIES_PROMPT,
    GET_SEVERITIES_PROMPT,
    UPDATE_POD_PROMPT,
)


def get_operations(zcp_api_wrapper: BaseAPIWrapper):
    operations: List[Dict] =[]
    if isinstance(zcp_api_wrapper, ZcpAnalysisAPIWrapper):
        operations: List[Dict] = [
            {
                "mode": "get_alerts",
                "name": "Get Alerts",
                "description": GET_ALERTS_PROMPT,
                "args_schema": GetAlerts,
            },
            {
                "mode": "get_priorities",
                "name": "Get Priorities",
                "description": GET_PRIORITIES_PROMPT,
                "args_schema": NoInput,
            },
            {
                "mode": "get_severities",
                "name": "Get Severities",
                "description": GET_SEVERITIES_PROMPT,
                "args_schema": NoInput,
            },
            {
                "mode": "get_alert_detail",
                "name": "Get Alert Detail",
                "description": GET_ALERT_DETAIL_PROMPT,
                "args_schema": GetAlertDetail,
            },
            {
                "mode": "get_channels",
                "name": "Get Channels",
                "description": GET_CHANNELS_PROMPT,
                "args_schema": GetChannels,
            },
            {
                "mode": "get_integrations",
                "name": "Get Integrations",
                "description": GET_INTEGRATIONS_PROMPT,
                "args_schema": GetIntegrations,
            },
        ]
    elif isinstance(zcp_api_wrapper, ZcpSelfHealingAPIWrapper):
        operations: List[Dict] = [
            {
                "mode": "alert_action",
                "name": "Alert Action",
                "description": ALERT_ACTION_PROMPT,
                "args_schema": AlertAction,
            },
            {
                "mode": "get_pods",
                "name": "Get Pods",
                "description": GET_PODS_PROMPT,
                "args_schema": GetPods,
            },
            {
                "mode": "create_pod",
                "name": "Create Pod",
                "description": CREATE_POD_PROMPT,
                "args_schema": CreatePod,
            },
            {
                "mode": "update_pod",
                "name": "Update Pod",
                "description": UPDATE_POD_PROMPT,
                "args_schema": UpdatePod,
            },
            {
                "mode": "delete_pod",
                "name": "Delete Pod",
                "description": DELETE_POD_PROMPT,
                "args_schema": DeletePod,
            },
        ]
    elif isinstance(zcp_api_wrapper, ZcpReportAPIWrapper):
        operations: List[Dict] = []
    else:
        raise ValueError(f"Invalid API wrapper: {type(zcp_api_wrapper)}")
    
    return operations
