from gapSolutions_client.logger import get_logger
from gapSolutions_client.constants import BASE_URL,base_token
from gapSolutions_client.utils import ApiErrorResponse, make_request
from gapSolutions_client.folder.folder_type import Folder

# Set up logging configuration
log = get_logger("gapSolutions_client.folder")

def folder_list(auth_token, query_params=None):
    """
    Retrieves a list of folders from an external API.
    """
    log.debug("folder_list() entry")
    url = f"{BASE_URL}/files/folders"
    response = make_request("GET", url, auth_token, query_params)

    if isinstance(response, ApiErrorResponse):
        log.error(f"API Error: {response.message}, Status Code: {response.status}")
        return response
    
    log.debug("folder_list() exit")
    return Folder.from_dict(response[0])



def folder_create(auth_token, folder_id, folder_title, query_params=None):
    """
    Creates a folder using the external API.
    """
    log.debug("folder_create() entry")
    url = f"{BASE_URL}/files/folders"
    data_payload = {"folder_id": folder_id, "folder_title": folder_title}
    response = make_request("POST", url, auth_token, query_params, data_payload)

    if isinstance(response, ApiErrorResponse):
        log.error(f"API Error: {response.message}, Status Code: {response.status}")
        log.debug("folder_create() exit")
        return response
    
    log.debug("folder_create() exit")
    return Folder.from_dict(response)
    


def folder_delete(auth_token, folder_id, query_params=None):
    """
    Deletes a folder using the external API.
    """
    log.debug("folder_delete() entry")
    url = f"{BASE_URL}/files/folders/{folder_id}"
    response = make_request("DELETE", url, auth_token, query_params)

    if isinstance(response, ApiErrorResponse):
        log.error(f"API Error: {response.message}, Status Code: {response.status}")
        log.debug("folder_delete() exit")
        return response
    
    log.debug("folder_delete() exit")
    return Folder.from_dict(response[0])

def folder_update(auth_token, folder_id, folder_data_text, query_params=None):
    """
    Updates a folder using the external API.
    """
    log.debug("folder_update() entry")
    url = f"{BASE_URL}/files/folders/{folder_id}"
    data_payload = {"folder": {"data": {"text": folder_data_text}}}
    response = make_request("PUT", url, auth_token, query_params, data_payload)

    if isinstance(response, ApiErrorResponse):
        log.error(f"API Error: {response.message}, Status Code: {response.status}")
        log.debug("folder_update() exit")
        return response
    
    log.debug("folder_update() exit")
    return Folder.from_dict(response[0])

def list_files_in_folder(auth_token, folder_id, query_params=None):
    """
    Retrieves a list of files in a specified folder using the external API.
    """
    default_params = {"all": "true", "lang": "en","sort":"filename|asc"}
    # Merge defaults with provided params
    query_params = {**default_params, **(query_params or {})}  

    log.debug("list_files_in_folder() entry")
    url = f"{BASE_URL}/files/folders/{folder_id}"
    
    response = make_request("GET", url, auth_token, query_params)

    if isinstance(response, ApiErrorResponse):
        log.error(f"API Error: {response.message}, Status Code: {response.status}")
        log.debug("list_files_in_folder() exit")
        return response
    
    # Handle empty response
    if not response:
        return response

    log.debug("list_files_in_folder() exit")
    return Folder.from_dict(response[0])


auth_token = base_token 
# response_json = folder_list(auth_token,query_params={"lang":"en"})
# response_json = list_files_in_folder(auth_token,36,query_params={"lang":"den"})
# response_json = folder_create(auth_token,8,"Test folder",query_params={"lang":"en"})
# response_json = folder_delete(auth_token,39,query_params={"lang":"en"})
# response_json = folder_update(auth_token,36,"Acc",query_params={"lang":"en"})
# print("response_json",response_json)
