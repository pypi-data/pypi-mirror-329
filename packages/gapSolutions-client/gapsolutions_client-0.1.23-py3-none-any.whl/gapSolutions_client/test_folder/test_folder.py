from unittest.mock import patch, MagicMock
from gapSolutions_client.folder.folder import folder_list, folder_create, folder_delete, folder_update, list_files_in_folder
from gapSolutions_client.utils import ApiErrorResponse,make_request
from gapSolutions_client.folder.folder_type import Folder

# Mocked response for successful API call
mock_success_response = {
    "id": 1,
    "account_id": 2,
    "title": "Test Folder",
    "permissions": None,
    "created_at": "2025-02-02T12:34:56",
    "updated_at": "2025-02-02T12:34:56",
    "key": "folder-key",
    "parent_folder_id": None,
    "all_childrens": None,
    "children": None
}

# Mocked error response for failed API call
mock_error_response = ApiErrorResponse(message="Not Found", status=404)

# Test folder_list function
@patch('gapSolutions_client.folder.folder.make_request')
def test_folder_list_success(mock_make_request):
    mock_make_request.return_value = [mock_success_response]  # Simulating success response
    
    result = folder_list(auth_token="dummy_token", query_params={"lang": "en"})
    
    assert isinstance(result, Folder)
    assert result.title == "Test Folder"
    assert result.id == 1
    assert result.account_id == 2


@patch('gapSolutions_client.folder.folder.make_request')
def test_folder_list_error(mock_make_request):
    mock_make_request.return_value = mock_error_response  # Simulating error response
    
    result = folder_list(auth_token="dummy_token", query_params={"lang": "en"})
    
    assert isinstance(result, ApiErrorResponse)
    assert result.message == "Not Found"
    assert result.status == 404


@patch('gapSolutions_client.folder.folder.make_request')
def test_folder_list_empty(mock_make_request):
    mock_make_request.return_value = []  # Simulating empty response
    
    result = list_files_in_folder(auth_token="dummy_token",folder_id=35, query_params={"lang": "en"})
    
    assert result == []


# Test folder_create function
@patch('gapSolutions_client.folder.folder.make_request')
def test_folder_create_success(mock_make_request):
    mock_make_request.return_value = mock_success_response  # Simulating success response
    
    result = folder_create(auth_token="dummy_token", folder_id=8, folder_title="Test Folder", query_params={"lang": "en"})
    
    assert isinstance(result, Folder)
    assert result.title == "Test Folder"
    assert result.id == 1


@patch('gapSolutions_client.folder.folder.make_request')
def test_folder_create_error(mock_make_request):
    mock_make_request.return_value = mock_error_response  # Simulating error response
    
    result = folder_create(auth_token="dummy_token", folder_id=8, folder_title="Test Folder", query_params={"lang": "en"})
    
    assert isinstance(result, ApiErrorResponse)
    assert result.message == "Not Found"
    assert result.status == 404


# Test folder_delete function
@patch('gapSolutions_client.folder.folder.make_request')
def test_folder_delete_success(mock_make_request):
    mock_make_request.return_value = [
    {
        "id": 1,
        "account_id": 52,
        "title": "Test Folder",
        "parent_folder_id": None,
        "permissions": None,
        "created_at": "2025-01-30T20:34:33.000000Z",
        "updated_at": "2025-01-30T20:34:33.000000Z",
        "key": "0",
        "all_childrens": None,
        "children": []
    }
]  # Simulating success response
    
    result = folder_delete(auth_token="dummy_token", folder_id=35, query_params={"lang": "en"})
    print("result",result)
    assert isinstance(result, Folder)
    assert result.title == "Test Folder"
    assert result.id == 1


@patch('gapSolutions_client.folder.folder.make_request')
def test_folder_delete_error(mock_make_request):
    mock_make_request.return_value = mock_error_response  # Simulating error response
    
    result = folder_delete(auth_token="dummy_token", folder_id=35, query_params={"lang": "en"})
    
    assert isinstance(result, ApiErrorResponse)
    assert result.message == "Not Found"
    assert result.status == 404


# Test folder_update function
@patch('gapSolutions_client.folder.folder.make_request')
def test_folder_update_success(mock_make_request):
    mock_make_request.return_value = [
    {
        "id": 36,
        "account_id": 52,
        "title": "Updated Folder Data",
        "parent_folder_id": None,
        "permissions": None,
        "created_at": "2025-01-30T20:34:33.000000Z",
        "updated_at": "2025-01-30T20:34:33.000000Z",
        "key": "0",
        "all_childrens": None,
        "children": []
    }
]  # Simulating success response
    
    result = folder_update(auth_token="dummy_token", folder_id=36, folder_data_text="Updated Folder Data", query_params={"lang": "en"})
    
    assert isinstance(result, Folder)
    assert result.title == "Updated Folder Data"
    assert result.id == 36

