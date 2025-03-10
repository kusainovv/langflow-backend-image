import requests
import json
import base64
from langflow.base.langchain_utilities.model import LCToolComponent
from langflow.schema import Data
from langflow.field_typing import Tool

class GetUDFTickerDataComponent(LCToolComponent):
    display_name = "Get UDF Ticker Data"
    description = ("Fetches the latest price data for a specified asset (e.g., BTC, ETH, DOGE) "
                   "using the Entangle UDF API. The asset symbol must be provided as a parameter.")
    name = "GetUDFTickerData"
    icon = "Entangle"
    
    def build_tool(self) -> Tool:
        return Tool(
            name="fetch_udf_ticker_data",
            func=self.run_model,
            description=("Fetch the latest price data for the given asset using Entangle UDF API. "
                         "Pass the asset symbol as parameter 'symbol' (e.g., 'BTC', 'ETH', 'DOGE').")
        )

    def decode_price(self, encoded_str: str) -> float:
        """Decodes the Base64-encoded price from UDF API response."""
        decoded_bytes = base64.b64decode(encoded_str)
        price_uint128 = int.from_bytes(decoded_bytes[-16:], byteorder='big')
        return price_uint128 / 10**18  # Normalize as per Ethereum-style scaling
    
    def run_model(self, symbol: str = "BTC", *args, **kwargs) -> Data:
        try:
            # Normalize the symbol to uppercase
            symbol = symbol.upper()
            url = f"https://udfsnap.ent-dx.com/last_votes?feedKeys={symbol}/USD"
            
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            
            # Extract the Base64-encoded value
            price_encoded = result["feeds"][0]["votes"][0]["Value"]
            
            # Decode the price
            price_decoded = self.decode_price(price_encoded)
            
            return Data(value={"symbol": symbol, "price": price_decoded})
        
        except requests.exceptions.RequestException as e:
            return Data(value=f"API request failed: {e}")
        except KeyError:
            return Data(value=f"Unexpected API response format for {symbol}")
        except Exception as e:
            return Data(value=f"Unexpected error: {e}")