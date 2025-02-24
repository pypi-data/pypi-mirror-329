from unittest.mock import patch, MagicMock
from gapSolutions_client.account.account import account_selection
from gapSolutions_client.utils import ApiErrorResponse,make_request
from gapSolutions_client.account.account_type import Account
from gapSolutions_client.constants import base_token
# Mocked response for successful API call
mock_success_response = [{
    "id": 281,
    "account_id": 52,
    "user_id": 1,
    "type": "admin",
    "last_log_in": "2025-01-15T08:01:57.000000Z",
    "created_at": "2024-12-18T13:47:11.000000Z",
    "updated_at": "2025-01-15T08:01:57.000000Z",
    "favorite": False,
    "role_id": 2,
    "account": {
        "id": 52,
        "name": "API Phyton account 1",
        "mergedStandardDescriptions": None
    }
}]

# Mocked error response for failed API call
mock_error_response = ApiErrorResponse(message="Not Found", status=404)


# Test folder_list function
def test_folder_account_e2e():
    # mock_make_request.return_value = [mock_success_response]  # Simulating success response
    
    result = account_selection(auth_token=base_token, query_params={"lang": "en"})
    
    assert isinstance(result, list)

# Test folder_list function
@patch('gapSolutions_client.account.account.make_request')
def test_folder_account_success(mock_make_request):
    mock_make_request.return_value = [mock_success_response]  # Simulating success response
    
    result = account_selection(auth_token="dummy_token", query_params={"lang": "en"})
    print("result",result)
    assert isinstance(result, list)
    assert isinstance(result[0], Account)
    assert result[0].id == 281


@patch('gapSolutions_client.account.account.make_request')
def test_folder_account_error(mock_make_request):
    mock_make_request.return_value = mock_error_response  # Simulating error response
    
    result = account_selection(auth_token="dummy_token", query_params={"lang": "en"})
    
    assert isinstance(result, ApiErrorResponse)
    assert result.message == "Not Found"
    assert result.status == 404


# @patch('gapSolutions_client.account.make_request')
# def test_folder_list_empty(mock_make_request):
#     mock_make_request.return_value = []  # Simulating empty response
    
#     result = list_files_in_folder(auth_token="dummy_token",folder_id=35, query_params={"lang": "en"})
    
#     assert result == []


# # Test folder_create function
# @patch('gapSolutions_client.account.make_request')
# def test_folder_create_success(mock_make_request):
#     mock_make_request.return_value = mock_success_response  # Simulating success response
    
#     result = folder_create(auth_token="dummy_token", folder_id=8, folder_title="Test Folder", query_params={"lang": "en"})
    
#     assert isinstance(result, Folder)
#     assert result.title == "Test Folder"
#     assert result.id == 1


# @patch('gapSolutions_client.account.make_request')
# def test_folder_create_error(mock_make_request):
#     mock_make_request.return_value = mock_error_response  # Simulating error response
    
#     result = folder_create(auth_token="dummy_token", folder_id=8, folder_title="Test Folder", query_params={"lang": "en"})
    
#     assert isinstance(result, ApiErrorResponse)
#     assert result.message == "Not Found"
#     assert result.status == 404


# # Test folder_delete function
# @patch('gapSolutions_client.account.make_request')
# def test_folder_delete_success(mock_make_request):
#     mock_make_request.return_value = [
#     {
#         "id": 1,
#         "account_id": 52,
#         "title": "Test Folder",
#         "parent_folder_id": None,
#         "permissions": None,
#         "created_at": "2025-01-30T20:34:33.000000Z",
#         "updated_at": "2025-01-30T20:34:33.000000Z",
#         "key": "0",
#         "all_childrens": None,
#         "children": []
#     }
# ]  # Simulating success response
    
#     result = folder_delete(auth_token="dummy_token", folder_id=35, query_params={"lang": "en"})
#     print("result",result)
#     assert isinstance(result, Folder)
#     assert result.title == "Test Folder"
#     assert result.id == 1


# @patch('gapSolutions_client.account.make_request')
# def test_folder_delete_error(mock_make_request):
#     mock_make_request.return_value = mock_error_response  # Simulating error response
    
#     result = folder_delete(auth_token="dummy_token", folder_id=35, query_params={"lang": "en"})
    
#     assert isinstance(result, ApiErrorResponse)
#     assert result.message == "Not Found"
#     assert result.status == 404


# # Test folder_update function
# @patch('gapSolutions_client.account.make_request')
# def test_folder_update_success(mock_make_request):
#     mock_make_request.return_value = [
#     {
#         "id": 36,
#         "account_id": 52,
#         "title": "Updated Folder Data",
#         "parent_folder_id": None,
#         "permissions": None,
#         "created_at": "2025-01-30T20:34:33.000000Z",
#         "updated_at": "2025-01-30T20:34:33.000000Z",
#         "key": "0",
#         "all_childrens": None,
#         "children": []
#     }
# ]  # Simulating success response
    
#     result = folder_update(auth_token="dummy_token", folder_id=36, folder_data_text="Updated Folder Data", query_params={"lang": "en"})
    
#     assert isinstance(result, Folder)
#     assert result.title == "Updated Folder Data"
#     assert result.id == 36


# # @patch('gapSolutions_client.account.make_request')
# # def test_folder_update_error(mock_make_request):
# #     mock_make_request.return_value = mock_error_response  # Simulating error response
    
# #     result = folder_u
