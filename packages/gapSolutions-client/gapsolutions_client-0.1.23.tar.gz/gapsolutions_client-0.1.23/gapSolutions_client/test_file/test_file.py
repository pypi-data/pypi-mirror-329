from unittest.mock import patch, MagicMock
from ..file.file import file_list,file_create,file_delete,file_update
from ..utils import ApiErrorResponse,make_request
from ..file.file_type import File
from ..constants import base_token
# Mocked response for successful API call
mock_success_response = [
    {
        "id": 20,
        "account_id": 52,
        "filename": "linkedIn2",
        "read_note": None,
        "path": "https://www.linkedin.com",
        "mime_type": "url",
        "size": 0,
        "created_at": "2025-01-12T10:00:40.000000Z",
        "updated_at": "2025-01-12T10:00:40.000000Z",
        "notes": None,
        "category_id": None,
        "fileable_id": None,
        "fileable_type": None,
        "additional_params": None,
        "force_download": 0,
        "category": None,
        "latest_version": {
            "id": 20,
            "file_id": 20,
            "version": 1,
            "status": "approvalflow_disabled",
            "read_note": None,
            "text": None,
            "filename": "linkedIn2",
            "path": "https://www.linkedin.com",
            "mime_type": "url",
            "size": 0,
            "created_at": "2025-01-12T10:00:40.000000Z",
            "updated_at": "2025-01-12T10:00:40.000000Z",
            "read_percent": None,
            "log_entry": None
        },
        "latest_approved_version": {
            "id": 20,
            "file_id": 20,
            "version": 1,
            "status": "approvalflow_disabled",
            "read_note": None,
            "text": None,
            "filename": "linkedIn2",
            "path": "https://www.linkedin.com",
            "mime_type": "url",
            "size": 0,
            "created_at": "2025-01-12T10:00:40.000000Z",
            "updated_at": "2025-01-12T10:00:40.000000Z",
            "read_percent": None
        },
        "versions": [
            {
                "id": 20,
                "file_id": 20,
                "version": 1,
                "status": "approvalflow_disabled",
                "read_note": None,
                "text": None,
                "filename": "linkedIn2",
                "path": "https://www.linkedin.com",
                "mime_type": "url",
                "size": 0,
                "created_at": "2025-01-12T10:00:40.000000Z",
                "updated_at": "2025-01-12T10:00:40.000000Z",
                "read_percent": None,
                "log_entry": None,
                "readers": []
            }
        ],
        "inspections": [],
        "link": {
            "id": 11,
            "file_id": 20,
            "url": "https://www.linkedin.com",
            "created_at": "2025-01-12T10:00:40.000000Z",
            "updated_at": "2025-01-12T10:00:40.000000Z"
        }
    }]

# Mocked error response for failed API call
mock_error_response = ApiErrorResponse(message="Not Found", status=404)


# Test file_list function
def test_file_account_e2e():
    # mock_make_request.return_value = [mock_success_response]  # Simulating success response
    
    result = file_list(auth_token=base_token, query_params={"lang": "en"})
    
    assert isinstance(result, list)

# Test file_create function
def test_file_create_e2e():
    # mock_make_request.return_value = [mock_success_response]  # Simulating success response
    
    result = file_create(auth_token=base_token,filename="samer10",url="www.facebook.com", query_params={"lang": "en"})
    
    # assert isinstance(result, list)

def test_file_delete_e2e():
    # mock_make_request.return_value = [mock_success_response]  # Simulating success response
    
    result = file_delete(auth_token=base_token,file_id=56, query_params={"lang": "en"})

def test_file_update_e2e():
    # mock_make_request.return_value = [mock_success_response]  # Simulating success response
    
    result = file_update(auth_toke=base_token,file_id=6,folder_id=31,filename="google", query_params={"lang": "en"})
    
# Test file_list function
@patch('gapSolutions_client.file.file.make_request')
def test_file_account_success(mock_make_request):
    mock_make_request.return_value = mock_success_response  # Simulating success response
    
    result = file_list(auth_token="dummy_token", query_params={"lang": "en"})
    print("result",result)
    assert isinstance(result, list)
    assert isinstance(result[0], File)
    assert result[0].id == 20


@patch('gapSolutions_client.file.file.make_request')
def test_file_list_error(mock_make_request):
    mock_make_request.return_value = mock_error_response  # Simulating error response
    
    result = file_list(auth_token="dummy_token", query_params={"lang": "en"})
    
    assert isinstance(result, ApiErrorResponse)
    assert result.message == "Not Found"
    assert result.status == 404


# @patch('gapSolutions_client.file.file.make_request')
# def test_folder_list_empty(mock_make_request):
#     mock_make_request.return_value = []  # Simulating empty response
    
#     result = list_files_in_folder(auth_token="dummy_token",folder_id=35, query_params={"lang": "en"})
    
#     assert result == []


# Test file_create function
@patch('gapSolutions_client.file.file.make_request')
def test_file_create_success(mock_make_request):
    mock_make_request.return_value = []  # Simulating success response
    
    result = file_create(auth_token="dummy_token", folder_id=8, filename="Test Folder", query_params={"lang": "en"})
    
    assert result == []


@patch('gapSolutions_client.file.file.make_request')
def test_file_create_error(mock_make_request):
    mock_make_request.return_value = mock_error_response  # Simulating error response
    
    result = file_create(auth_token="dummy_token", folder_id=8, filename="Test Folder", query_params={"lang": "en"})
    
    assert isinstance(result, ApiErrorResponse)
    assert result.message == "Not Found"
    assert result.status == 404


# # Test file_delete function
@patch('gapSolutions_client.file.file.make_request')
def test_file_delete_success(mock_make_request):
    mock_make_request.return_value = []  # Simulating success response
    
    result = file_delete(auth_token="dummy_token", file_id=35, query_params={"lang": "en"})
    assert isinstance(result, list)
    assert result == []


@patch('gapSolutions_client.file.file.make_request')
def test_file_delete_error(mock_make_request):
    mock_make_request.return_value = mock_error_response  # Simulating error response
    
    result =file_delete(auth_token="dummy_token", file_id=35, query_params={"lang": "en"})
    
    assert isinstance(result, ApiErrorResponse)
    assert result.message == "Not Found"
    assert result.status == 404


# Test file_update function
@patch('gapSolutions_client.file.file.make_request')
def test_folder_update_success(mock_make_request):
    mock_make_request.return_value = []  # Simulating success response
    
    result = file_update(auth_token="dummy_token", file_id=36, filename="Updated Folder Data", query_params={"lang": "en"})
    
    assert isinstance(result, list)
    assert result == []

