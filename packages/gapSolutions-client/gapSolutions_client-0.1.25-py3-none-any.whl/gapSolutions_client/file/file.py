from ..logger import get_logger
from ..constants import BASE_URL,base_token
from ..utils import ApiErrorResponse, make_request
from ..file.file_type import File

# Set up logging configuration
log = get_logger("gapSolutions_client.file")

def file_list(auth_token, query_params=None):
    """
    Retrieves a list of files from an external API.
    """
    log.debug("file_list() entry")
    url = f"{BASE_URL}/files"

    default_params = {"all": "false", "lang": "en","sort":"filename|asc"}
    # Merge defaults with provided params
    query_params = {**default_params, **(query_params or {})}  
    response = make_request("GET", url, auth_token, query_params)

    if isinstance(response, ApiErrorResponse):
        log.error(f"API Error: {response.message}, Status Code: {response.status}")
        log.debug("file_list() exit")
        return response
    
    if query_params.get("all") == "true":
        log.info("Query parameter 'all' is set to 'true'.")
        response = response[0].get("data", [])
    files = []   
    if response:
        files = [File.from_dict(account) for account in response]
        

    log.debug("file_list() exit")
    return files


def file_create(auth_token,
                filename,
                file=None,
                status=None,
                note=None,
                folder_id=None,
                url=None,
                query_params=None):
    """
    create a file from an external API.
    """
    log.debug("file_create() entry")
    url = f"{BASE_URL}/files"

    default_params = {"lang": "en"}
    # Merge defaults with provided params
    data_payload = {key: value for key, value in {
        "filename": filename,
        "file": file,
        "status": status,
        "note": note,
        "folder_id": folder_id,
        "url": url
    }.items() if value is not None}

    query_params = {**default_params, **(query_params or {})}  
    response = make_request("POST", url, auth_token, query_params,data_payload)
    if isinstance(response, ApiErrorResponse):
        log.error(f"API Error: {response.message}, Status Code: {response.status}")
        return response
    
    return response

def file_update(auth_token,
                file_id,
                filename,
                file=None,
                note=None,
                folder_id=None,
                url=None,
                query_params=None):
    """
    create a file from an external API.
    """
    log.debug("file_update() entry")
    url = f"{BASE_URL}/files/{file_id}"

    default_params = {"lang": "en"}
    # Merge defaults with provided params
    data_payload = {
        "_method": "PATCH",  # Always included
        **{key: value for key, value in {
            "filename": filename,
            "file": file,
            "note": note,
            "folder_id": folder_id,
            "url": url
        }.items() if value is not None}
    }
    print("data_payload",data_payload)
    query_params = {**default_params, **(query_params or {})}  
    response = make_request("POST", url, auth_token, query_params,data_payload)
    if isinstance(response, ApiErrorResponse):
        log.error(f"API Error: {response.message}, Status Code: {response.status}")
        log.debug("file_update() exit")

        return response
    
    log.debug("file_update() exit")
    return response

def file_delete(auth_token,
                file_id,
                query_params=None):
    """
    delete a file from an external API.
    """
    log.debug("file_delete() entry")
    url = f"{BASE_URL}/files/{file_id}"
    print("url",url)
    default_params = {"lang": "en"}

    # Merge defaults with provided params
    query_params = {**default_params, **(query_params or {})}  
    response = make_request("DELETE", url, auth_token, query_params)
    if isinstance(response, ApiErrorResponse):
        log.error(f"API Error: {response.message}, Status Code: {response.status}")
        log.debug("file_delete() exit")
        return response
    
    log.debug("file_delete() exit")
    return response

auth_token = base_token 
# response_json = file_list(auth_token,query_params={"all": "true","lang":"en"})
# response_json = file_create(auth_token,query_params={"all": "true","lang":"en"})
# print("response_json",response_json)
