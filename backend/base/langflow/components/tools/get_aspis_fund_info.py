import requests
from langflow.schema import Data
from langflow.inputs import SecretStrInput, MessageTextInput
from langflow.custom import Component
from langflow.template import Output

class GetAspisFundInfoComponent(Component):
    display_name = "Get Aspis Vault Fund Info"
    description = (
        "Retrieve detailed information about a vault fund from the Aspis API by providing the **specific vault address** and an **API key**. "
        "This includes details like asset allocation, current holdings, and liquidity."
    )
    name = "GetAspisVaultFundInfo"
    icon = "ASPIS"

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="API Key",
            info=(
                "**Provide the secret API key for Aspis API authentication.**\n"
                "- Required in the format: 'using my Aspis API key: YOUR_API_KEY'.\n"
                "- Example: 'using my Aspis API key: dQzHaWL9yj7ZCqvWVv7201CMDasJFzaM3CN9wWx8'.\n"
                "This key authenticates requests to fetch sensitive vault information."
            ),
            required=True,
        ),
        MessageTextInput(
            name="vault_address",
            display_name="Vault Address",
            info=(
                "**Provide the Ethereum vault address of the fund you want to query.**\n"
                "- Required in the format: 'vault address VAULT_ADDRESS'.\n"
                "- Example: 'vault address 0x315F419f0BA5d47FC65d5f930EC4b9912579709F'.\n"
                "This address identifies the vault fund to retrieve data for."
            ),
            required=True,
            tool_mode=True
        )
    ]

    outputs = [
        Output(name="fund_info", display_name="Detailed Fund Information", method="fetch_vault_fund_info"),
    ]

    def fetch_vault_fund_info(self) -> Data:
        """
        Fetch detailed vault fund information using the API key and vault address.
        """
        api_key = self.api_key
        vault_address = self.vault_address.replace("vault address", "").strip()

        print(f"DEBUG: API Key - {api_key}, Vault Address - {vault_address}")

        try:
            url = f"https://v2api.aspis.finance/api/fund?address={vault_address}"
            headers = {
                "x-api-key": api_key,
                "accept": "application/json",
            }

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            return Data(value={"result": response.json()})

        except requests.exceptions.RequestException as e:
            return Data(value={"error": f"API request failed: {e}"})
        except Exception as e:
            return Data(value={"error": f"Unexpected error: {e}"})