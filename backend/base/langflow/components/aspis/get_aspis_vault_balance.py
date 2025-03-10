import requests
from langflow.schema import Data
from langflow.inputs import SecretStrInput, MessageTextInput
from langflow.custom import Component
from langflow.template import Output


class GetAspisVaultBalanceComponent(Component):
    display_name = "Get Aspis Vault Balance"
    description = "Fetches the current balance of an Aspis Vault using API key, chain ID, and vault address."
    name = "GetAspisVaultBalance"
    icon = "ASPIS"

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="API Key",
            info="The API key to authenticate the request.",
            required=True,
        ),
        MessageTextInput(
            name="chain_id",
            display_name="Chain ID",
            info="The blockchain chain ID where the Aspis Vault resides.",
            required=True,
            tool_mode=True,
        ),
        MessageTextInput(
            name="vault_address",
            display_name="Vault Address",
            info="The Ethereum address of the Aspis Vault.",
            required=True,
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(
            name="vault_balance",
            display_name="Vault Balance",
            method="_fetch_vault_balance",
            description=(
                "Returns the balance of the specified Aspis Vault. The output is a JSON object "
                "containing details about the vault's balance, including token holdings and other information."
            ),
        ),
    ]

    def _fetch_vault_balance(self) -> Data:
        """
        Dynamically destructures the input arguments and fetches the vault balance.
        """
        api_key = self.api_key
        chain_id = self.chain_id
        vault_address = self.vault_address

        print("DEBUG: Received Inputs")
        print(f"API Key: {api_key}")
        print(f"Chain ID: {chain_id}")
        print(f"Vault Address: {vault_address}")

        try:
            url = f"https://trading-api.aspis.finance/get_balance?chainId={chain_id}&vault={vault_address}"
            headers = {
                "x-api-key": api_key,
                "accept": "application/json",
            }

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            return Data(data={"result": response.json()})

        except requests.exceptions.RequestException as e:
            return Data(value={"error": f"API request failed: {e}"})
        except Exception as e:
            return Data(value={"error": f"Unexpected error: {e}"})