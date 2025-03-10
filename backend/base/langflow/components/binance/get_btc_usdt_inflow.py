import requests
from langflow.base.langchain_utilities.model import LCToolComponent
from langflow.schema import Data
from langflow.field_typing import Tool


class GetBTCUSDTInflowComponent(LCToolComponent):
    display_name = "Get BTC/USDT Inflow"
    description = "Fetches the latest net inflow value for the BTC/USDT pair using Binance API."
    name = "GetBTCUSDTInflow"
    icon = "Binance"
    
    def build_tool(self) -> Tool:
        return Tool(
            name="fetch_btcusdt_inflow",
            func=self.run_model,
            description="Fetch the latest net inflow value for the BTC/USDT pair using Binance API."
        )

    def run_model(self, *args, **kwargs) -> Data:
        try:
            url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
            response = requests.get(url)
            response.raise_for_status()

            result = response.json()
            net_inflow = result.get("quoteVolume")  

            return Data(value=f"Net inflow (quote volume): {net_inflow}")

        except requests.exceptions.RequestException as e:
            return Data(value=f"API request failed: {e}")
        except Exception as e:
            return Data(value=f"Unexpected error: {e}")