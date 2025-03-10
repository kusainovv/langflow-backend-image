import requests
from langflow.base.langchain_utilities.model import LCToolComponent
from langflow.field_typing import Tool
from langflow.schema import Data

class GetFearGreedComponent(LCToolComponent):
    display_name = "Get Fear Greed"
    description = "Fetches the latest Fear and Greed Index value using an external API."
    name = "GetFearGreed"
    icon = "Entangle"
    
    def build_tool(self) -> Tool:
        return Tool(
            name="GetFearGreedTool",
            description="Fetches the latest Fear and Greed Index value.",
            func=self.run_model  
        )

    def run_model(self, *args, **kwargs) -> Data:
        try:
            url = "https://api.alternative.me/fng/"
            response = requests.get(url)
            response.raise_for_status()

            result = response.json()
            fear_greed_value = result["data"][0]["value"]

            return Data(value=f"Fear and Greed Index: {fear_greed_value}")

        except requests.exceptions.RequestException as e:
            return Data(value=f"API request failed: {e}")
        except Exception as e:
            return Data(value=f"Unexpected error: {e}")