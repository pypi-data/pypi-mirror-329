from typing import Literal, Optional, List
from pydantic import BaseModel, Field


class NoInput(BaseModel):
    pass


class GetAlerts(BaseModel):
    statuses: list[str] = Field(
        None, title="alert status", description="Search query string for status"
    )
    senders: list[str] = Field(
        None, title="alert sender", description="Search query string for sender"
    )
    priorities: list[str] = Field(
        None,
        title="alert priority",
        description="Search query string for alert priority",
    )
    severities: list[str] = Field(
        None,
        title="alert severity",
        description="Search query string for alert severity",
    )
    fingerprint: Optional[str] = Field(
        None,
        max_length=36,
        title="alert fingerprint",
        description="Search query string for fingerprint. The max length is 36",
    )
    alert_id: Optional[str] = Field(
        None,
        max_length=100,
        title="alert id",
        description="Search query string for fingerprint. The max length is 100",
    )
    repeated_count: Optional[int] = Field(
        None,
        le=10000,
        title="alert repeated count",
        description="Search query string for repeated count, Should be less than 10000",
    )
    repeated_count_operator: Literal["gte", "gt", "lte", "lt"] = Field(
        None,
        title="alert repeated count operator",
        description="Search query string for repeated count operator",
    )
    alertname: Optional[str] = Field(
        None,
        max_length=100,
        title="alert name",
        description="Search query string for alert name. The max length is 100",
    )
    description: Optional[str] = Field(
        None,
        max_length=100,
        title="alert description",
        description="Search query string for alert description. The max length is 100",
    )
    summary: Optional[str] = Field(
        None,
        max_length=100,
        title="alert summary",
        description="Search query string for alert summary. The max length is 100",
    )
    project: Optional[str] = Field(
        None,
        max_length=100,
        title="alert project",
        description="Search query string for alert project. The max length is 100",
    )
    clusters: list[str] = Field(
        None,
        title="alert clusters",
        description="Search query string for alert clusters",
    )
    namespaces: list[str] = Field(
        None,
        title="alert namespaces",
        description="Search query string for alert namespaces",
    )
    start_date: Optional[str] = Field(
        None,
        title="search start date",
        description="Search query string for start date (ISO 8601 format(e.g. 2024-11-05T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    )
    end_date: Optional[str] = Field(
        None,
        title="search end date",
        description="Search query string for end date (ISO 8601 format(e.g. 2024-11-06T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    )
    start_date_created_at: Optional[str] = Field(
        None,
        title="search start date",
        description="Search query string for start date (ISO 8601 format(e.g. 2024-11-05T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    )
    end_date_created_at: Optional[str] = Field(
        None,
        title="search end date",
        description="Search query string for end date (ISO 8601 format(e.g. 2024-11-06T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    )
    start_date_closed_at: Optional[str] = Field(
        None,
        title="search start date",
        description="Search query string for start date (ISO 8601 format(e.g. 2024-11-05T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    )
    end_date_closed_at: Optional[str] = Field(
        None,
        title="search end date",
        description="Search query string for end date (ISO 8601 format(e.g. 2024-11-06T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    )
    labels: list[str] = Field(
        None,
        title="search labels",
        description="Search query string for labels e.g. severity:critical,priority:P1",
    )
    sort_field: Optional[str] = Field(
        None, title="sort field", description="Sort field name"
    )
    sort_direction: Optional[str] = Field(
        None, title="sort direction", description="Sort direction"
    )
    page_number: int = Field(
        None,
        # ge=1,
        # title="page number",
        description="Page number. Default is 1 and it should be greater than 0",
    )
    page_size: int = Field(
        None,
        # ge=10,
        # le=500,
        # title="page size",
        description="Page size. Default is 10 and it should be greater than 10 and less than 500",
    )


class GetAlertDetail(BaseModel):
    alert_id: str = Field(
        None,
        title="alert id",
        description="Search query string for alert id",
    )


class GetChannels(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=100,
        title="channel name",
        description="Search query string for name. The max length is 100",
    )
    types: Optional[List[str]] = Field(
        None, title="channel type", description="Search query string for type"
    )
    sort_field: Optional[str] = Field(
        "name", title="sort field", description="Sort field name"
    )
    sort_direction: Optional[str] = Field(
        "asc", title="sort direction", description="Sort direction"
    )
    page_number: Optional[int] = Field(
        1,
        ge=1,
        title="page number",
        description="Page number. Default is 1 and it should be greater than 0",
    )
    page_size: Optional[int] = Field(
        10,
        ge=10,
        le=500,
        title="page size",
        description="Page size. Default is 10 and it should be greater than 10 and less than 500",
    )


class GetIntegrations(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=100,
        title="channel name",
        description="Search query string for name. The max length is 100",
    )
    channel_name: Optional[str] = Field(
        None,
        max_length=100,
        title="channel name",
        description="Search query string for channel name. The max length is 100",
    )
    channel_type: Optional[str] = Field(
        None, title="channel type", description="Search query string for channel type."
    )
    status: Optional[str] = Field(
        None, title="integration status", description="Search query string for status"
    )
    sort_field: Optional[str] = Field(
        "name", title="sort field", description="Sort field name"
    )
    sort_direction: Optional[str] = Field(
        "asc", title="sort direction", description="Sort direction"
    )
    page_number: Optional[int] = Field(
        1,
        ge=1,
        title="page number",
        description="Page number. Default is 1 and it should be greater than 0",
    )
    page_size: Optional[int] = Field(
        10,
        ge=10,
        le=500,
        title="page size",
        description="Page size. Default is 10 and it should be greater than 10 and less than 500",
    )


class AlertAction(BaseModel):
    alert_id: str = Field(
        None,
        title="alert id",
        description="Alert id"
    )
    action: str = Field(
        None,
        title="action",
        description="Action enum"
    )
    snoozed_until_at: Optional[str] = Field(
        None,
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
        title="snoozed time",
        description="Snoozed time (ISO 8601 format(e.g. 2024-11-05T14:48:00.000+09:00))"
    )
