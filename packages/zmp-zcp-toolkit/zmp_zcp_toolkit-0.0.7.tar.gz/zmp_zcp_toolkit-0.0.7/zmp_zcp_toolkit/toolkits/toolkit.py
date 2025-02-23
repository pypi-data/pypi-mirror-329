from __future__ import annotations

import re
from typing import Dict, List

from langchain_core.tools import BaseTool
from langchain_core.tools.base import BaseToolkit

from zmp_zcp_toolkit.tools.tool import ZcpTool
from zmp_zcp_toolkit.wrapper.operations import get_operations
from zmp_zcp_toolkit.wrapper.base_wrapper import BaseAPIWrapper


class ZcpToolkit(BaseToolkit):
    tools: List[BaseTool] = []

    @classmethod
    def from_zcp_api_wrapper(cls, *, zcp_api_wrapper: BaseAPIWrapper) -> "ZcpToolkit":
        """Create a ZcpToolkit from a ZCP Analysis API wrapper.

        Args:
            zcp_api_wrapper (ZcpBaseAPIWrapper): The ZCP API wrapper instance which extends ZcpBaseAPIWrapper to use

        Returns:
            ZcpToolkit: A toolkit containing tools for interacting with the ZCP Analysis API
        """

        operations: List[Dict] = get_operations()

        tools = [
            ZcpTool(
                name=re.sub(r"[^a-zA-Z0-9_-]", "_", action["name"]),
                description=action["description"],
                mode=action["mode"],
                api_wrapper=zcp_api_wrapper,
                args_schema=action.get("args_schema", None),
            )
            for action in operations
        ]

        return cls(tools=tools)

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return self.tools
