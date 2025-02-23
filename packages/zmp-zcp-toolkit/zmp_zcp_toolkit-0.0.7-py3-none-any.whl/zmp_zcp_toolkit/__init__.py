import logging

from .wrapper.base_wrapper import AuthenticationType
from .wrapper.api_wrapper import ZcpAnalysisAPIWrapper, ZcpReportAPIWrapper
from .toolkits.toolkit import ZcpToolkit
from .tools.tool import ZcpTool


__all__ = [
    "ZcpAnalysisAPIWrapper",
    "ZcpReportAPIWrapper",
    "ZcpToolkit",
    "ZcpTool",
    "AuthenticationType",
]

__logger_name = "zmp_zcp_toolkit"


def configure_logging(level=logging.INFO):
    """Configure logging for the library

    Args:
        level (logging.LEVEL, optional): The logging level to use. Defaults to logging.INFO.
    """

    logger = logging.getLogger(__logger_name)
    logger.setLevel(level)
