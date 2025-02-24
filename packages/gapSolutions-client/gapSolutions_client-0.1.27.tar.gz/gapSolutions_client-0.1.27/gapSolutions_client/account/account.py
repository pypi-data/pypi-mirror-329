from gapSolutions_client.logger import get_logger
from gapSolutions_client.constants import BASE_URL,base_token
from gapSolutions_client.utils import ApiErrorResponse, make_request
from gapSolutions_client.account.account_type import Account

# Set up logging configuration
log = get_logger("gapSolutions_client.folder")

def account_selection(auth_token, query_params=None):
    """
    Retrieves a list of accounts from an external API.
    """
    log.debug("account_selection() entry")
    url = f"{BASE_URL}/account-selection"
    response = make_request("GET", url, auth_token, query_params)
    if isinstance(response, ApiErrorResponse):
        log.error(f"API Error: {response.message}, Status Code: {response.status}")
        return response
    
    # Convert entire list of accounts from dict
    accounts = [Account.from_dict(account) for account in response[0]]
    log.debug("account_selection() exit")
    print("accounts",accounts)
    return accounts


auth_token = base_token 
# response_json = account_selection(auth_token,query_params={"lang":"en"})
# print("response_json",response_json)
