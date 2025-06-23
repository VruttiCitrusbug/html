import logging
import asyncio
from azure.identity import DeviceCodeCredential
from msgraph.core import GraphClient
from msgraph.core._auth import AuthProvider

logger = logging.getLogger("GraphInterface")
logging.basicConfig(level=logging.INFO)

graph_client = None
auth_provider = None


def initialize_graph_auth(application_id: str, scopes: list[str], tenant_id: str):
    global graph_client, auth_provider

    try:
        credential = DeviceCodeCredential(
            client_id=application_id,
            tenant_id=tenant_id,
            prompt_callback=lambda challenge: logger.info(challenge["message"])
        )

        auth_provider = AuthProvider(credential, scopes=scopes)
        graph_client = GraphClient(auth_provider=auth_provider)

    except Exception as e:
        logger.error(str(e))
        raise


async def get_user_access_token() -> str:
    try:
        token = await auth_provider._credential.get_token(*auth_provider._scopes)
        return token.token
    except Exception as ex:
        logger.error(str(ex))
        raise


# Example usage (uncomment below to run):
initialize_graph_auth('739f8334-684c-4ccf-b5d5-78902021056d', ['User.Read'], '6044f6c7-6021-4df8-a108-ff5499f32368')
# token = asyncio.run(get_user_access_token())
# print("Access Token:", token)