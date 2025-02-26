from typing import Any, Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from zmp_zcp_toolkit.wrapper.base_wrapper import BaseAPIWrapper


class ZcpTool(BaseTool):  # type: ignore[override]
    """Tool for interacting with the ZCP API.

    This tool provides an interface to execute operations against a ZCP API endpoint.
    It supports different modes of operation and can handle both schema-validated
    and raw instruction inputs.

    Attributes:
        api_wrapper (ZcpBaseAPIWrapper): The wrapper instance for making API calls
        mode (str): The operation mode to execute (e.g. "get_alerts", "get_priorities")
        name (str): Display name of the tool
        description (str): Detailed description of what the tool does
        args_schema (Optional[Type[BaseModel]]): Pydantic model for validating input arguments
    """

    api_wrapper: BaseAPIWrapper = Field(default_factory=BaseAPIWrapper)  # type: ignore[arg-type]
    mode: str = Field(..., description="The operation mode to execute")
    name: str = Field(None, description="Display name of the tool")
    description: str = Field(
        None, description="Detailed description of what the tool does"
    )
    args_schema: Optional[Type[BaseModel]] = Field(
        None, description="Pydantic model for validating input arguments"
    )

    def _run(
        self,
        instructions: Optional[str] = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
        **kwargs: Any,
    ) -> str:
        """Run the ZCP tool with the given instructions.

        Args:
            instructions (Optional[str], optional): Instructions or parameters to pass to the ZCP API. Defaults to "".
            run_manager (Optional[CallbackManagerForToolRun], optional): Callback manager for the tool run. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the API wrapper.

        Returns:
            str: Response from the ZCP API after executing the instructions.
        """
        if not instructions or instructions == "{}":
            instructions = ""

        if self.args_schema is not None:
            query = self.args_schema(**kwargs)
        else:
            query = instructions

        return self.api_wrapper.run(self.mode, query)
