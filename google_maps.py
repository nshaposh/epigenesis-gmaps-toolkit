from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type

from google_maps_wrapper import GoogleMapsWrap
from superagi.helper.token_counter import TokenCounter
from superagi.llms.base_llm import BaseLlm
from superagi.models.agent_execution import AgentExecution
from superagi.models.agent_execution_feed import AgentExecutionFeed
from superagi.tools.base_tool import BaseTool

class GoogleMapsInput(BaseModel):
    query: str = Field(..., description="Google Maps Search Query.")

class GoogleMapsSearchTool(BaseTool):
    """
    Google Maps Search tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    llm: Optional[BaseLlm] = None
    name = "GoogleSearch"
    agent_id: int = None
    agent_execution_id: int = None
    description = (
        "A tool for performing a Google Maps search and extracting addresses and places details."
        "Input should be a search query."
    )
    args_schema: Type[GoogleMapsSchema] = GoogleMapsInput

    class Config:
        arbitrary_types_allowed = True

    def _execute(self, query: str) -> Any:
        """
        Execute the Google search tool.

        Args:
            query : The query to search for.

        Returns:
            Search result summary
        """
        api_key = self.get_tool_config("GOOGLE_PLACES_API_KEY")
        num_results = 5

        google_maps_search = GoogleMapsWrap(api_key, num_results)
        places = google_maps_search.get_result(query)

        return "\n".join([f"{i+1}. {item}" for i, item in enumerate(places)])