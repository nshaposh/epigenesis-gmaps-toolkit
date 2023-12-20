#import logging
import time
from pydantic import BaseModel
from typing import Any, Dict, Optional
from superagi.lib.logger import logger
#from logger import logger
import googlemaps

from superagi.helper.webpage_extractor import WebpageExtractor

class GoogleMapsWrap:

    def __init__(self, api_key, num_results=3):
        """
        Initialize the GoogleSearchWrap class.

        Args:
            api_key (str): Google Places API key
            num_results (int): Number of results per page
            num_pages (int): Number of pages to search
            num_extracts (int): Number of extracts to extract from each webpage
        """

        self.api_key = api_key
        self.top_k_results = num_results     
        self.google_map_client = googlemaps.Client(key=self.api_key)

    def get_result(self, query):
        """
        Run the Google Maps search.

        Args:
            query (str): The query to search for
            k: number of places to return.

        Returns:
            list: A list of extracts from the search results.
        """
        
        search_results = self.google_map_client.places(query)["results"][0:k]
        num_to_return = len(search_results)

        places = []

        if num_to_return == 0:
            return "Google Places did not find any places that match the description"

        num_to_return = (
            num_to_return
            if self.top_k_results is None
            else min(num_to_return, self.top_k_results)
        )

        for i in range(num_to_return):
            result = search_results[i]
            details = self.fetch_place_details(result["place_id"])

            if details is not None:
                places.append(details)

        #return "\n".join([f"{i+1}. {item}" for i, item in enumerate(places)])
        return places

    def fetch_place_details(self, place_id: str) -> Optional[str]:
        try:
            place_details = self.google_map_client.place(place_id)
            formatted_details = self.format_place_details(place_details)
            return formatted_details
        except Exception as e:
            logger.error(f"An Error occurred while fetching place details: {e}")
            return None

    def format_place_details(self, place_details: Dict[str, Any]) -> Optional[str]:
        try:
            name = place_details.get("result", {}).get("name", "Unkown")
            address = place_details.get("result", {}).get(
                "formatted_address", "Unknown"
            )
            phone_number = place_details.get("result", {}).get(
                "formatted_phone_number", "Unknown"
            )
            website = place_details.get("result", {}).get("website", "Unknown")

            formatted_details = (
                f"{name}\nAddress: {address}\n"
                f"Phone: {phone_number}\nWebsite: {website}\n\n"
            )
            return formatted_details
        except Exception as e:
            logger.error(f"An error occurred while formatting place details: {e}")
            return None