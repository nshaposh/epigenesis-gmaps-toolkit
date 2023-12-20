from abc import ABC
from typing import List
from superagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from google_maps import GoogleMapsSearchTool
from superagi.models.tool_config import ToolConfig
from superagi.types.key_type import ToolConfigKeyType


class GoogleMapsToolkit(BaseToolkit, ABC):
    name: str = "Google Maps Search Toolkit"
    description: str = "Toolkit containing tools for performing Google Maps search and extracting addresses and information about places"

    def get_tools(self) -> List[BaseTool]:
        return [GoogleMapsSearchTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return [
            ToolConfiguration(key="GOOGLE_PLACES_API_KEY", key_type=ToolConfigKeyType.STRING, is_required= True, is_secret = True),
        ]