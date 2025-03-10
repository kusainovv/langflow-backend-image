import requests
from langflow.schema import Data
from langflow.io import MessageTextInput
from langflow.inputs import SecretStrInput
from langflow.custom import Component
from langflow.template import Output

class GetAspisExecuteOrderComponent(Component):
    display_name = "Get Aspis Execute Order"
    description = "Executes buy/sell transactions via the Aspis Vault using the provided API key and parameters."
    name = "GetAspisExecuteOrder"
    icon = "ASPIS"

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="API Key",
            info="API key for authentication with Aspis API.",
            required=True,
        ),
        MessageTextInput(
            name="chain_id",
            display_name="Chain ID",
            info="The chain ID associated with the Aspis Vault.",
            required=True,
            tool_mode=True
        ),
        MessageTextInput(
            name="vault_address",
            display_name="Vault Address",
            info="The vault address to execute the transaction.",
            required=True,
            tool_mode=True
        ),
        MessageTextInput(
            name="src_token",
            display_name="Source Token",
            info="The token to exchange (e.g., USDT, WETH, WBTC).",
            required=True,
            tool_mode=True,
        ),
        MessageTextInput(
            name="dst_token",
            display_name="Destination Token",
            info="The token to receive (e.g., USDT, WETH, WBTC).",
            required=True,
            tool_mode=True,
        ),
        MessageTextInput(
            name="amount_in",
            display_name="Amount In",
            info="The amount of the source token to exchange.",
            required=True,
            tool_mode=True,
        ),
        MessageTextInput(
            name="exchange",
            display_name="Exchange",
            info="The DEX to execute the operation (1INCH, UNISWAP, ODOS).",
            required=True,
            tool_mode=True,
        ),
        MessageTextInput(
            name="slippage",
            display_name="Slippage",
            info="The slippage value for the transaction (default is 0.5).",
            required=True,
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(name="transaction_data", display_name="Transaction Data", method="execute_order"),
    ]

    def execute_order(self) -> Data:
        """
        Executes a buy/sell transaction via the Aspis Vault using the provided parameters.
        """
        try:
            url = "https://trading-api.aspis.finance/execute_order"

            headers = {
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
            }

            payload = {
                "chainId": self.chain_id,
                "vault": self.vault_address,
                "srcToken": self.src_token,
                "dstToken": self.dst_token,
                "amountIn": self.amount_in,
                "exchange": self.exchange,
                "slippage": self.slippage,
            }

            print("DEBUG: Payload ->", payload)
            print("DEBUG: Headers ->", headers)

            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()

            return Data(value={"result": response.json()})

        except requests.exceptions.RequestException as e:
            return Data(value={"error": f"API request error: {e}"})
        except Exception as e:
            return Data(value={"error": f"Unexpected error: {e}"})