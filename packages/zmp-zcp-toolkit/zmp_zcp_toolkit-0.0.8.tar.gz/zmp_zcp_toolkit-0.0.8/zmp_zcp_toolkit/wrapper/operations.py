from typing import Dict, List

from zmp_zcp_toolkit.wrapper.parameters import GetAlerts, NoInput, GetAlertDetail, GetChannels, GetIntegrations, AlertAction
from zmp_zcp_toolkit.wrapper.prompts import (
    GET_ALERTS_PROMPT,
    GET_ALERT_DETAIL_PROMPT,
    GET_PRIORITIES_PROMPT,
    GET_SEVERITIES_PROMPT,
    GET_CHANNELS_PROMPT,
    GET_INTEGRATIONS_PROMPT,
    ALERT_ACTION_PROMPT,
)


def get_operations():
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
        {
            "mode": "alert_action",
            "name": "Alert Action",
            "description": ALERT_ACTION_PROMPT,
            "args_schema": AlertAction,
        },
    ]

    return operations
