import requests
from langflow.schema import Data
from langflow.io import MessageTextInput
from langflow.custom import Component
from langflow.template import Output

class GetAspisRatesComponent(Component):
    display_name = "Get Aspis Asset Rate"
    description = "Fetches the rate of a specified asset from the Aspis API in USD."
    name = "GetAspisAssetRate"
    icon = "ASPIS"

    inputs = [
        MessageTextInput(
            name="asset_name",
            display_name="Asset Name",
            info="Enter the asset symbol (e.g., BTC, ETH) to fetch its rate in USD.",
            required=True,
            tool_mode=True
        )
    ]

    outputs = [
        Output(name="asset_rate", display_name="Asset Rate in USD", method="fetch_asset_rate"),
    ]

    def fetch_asset_rate(self) -> Data:
        """
        Fetch the rate of the specified asset from the Aspis API.
        """
        asset_name = self.asset_name

        try:
            url = "https://v2api.aspis.finance/api/rates"
            response = requests.get(url)
            response.raise_for_status()

            rates = response.json()

            # Extract the rate for the specified asset
            asset_rate = rates["data"].get(asset_name.upper(), {}).get("USD")
            if asset_rate:
                return Data(value={"result": f"The rate of {asset_name.upper()} is ${asset_rate} USD"})
            else:
                return Data(value={"error": f"Rate for asset '{asset_name}' not found in API response."})

        except requests.exceptions.RequestException as e:
            return Data(value={"error": f"API request error: {e}"})
        except Exception as e:
            return Data(value={"error": f"Unexpected error: {e}"})