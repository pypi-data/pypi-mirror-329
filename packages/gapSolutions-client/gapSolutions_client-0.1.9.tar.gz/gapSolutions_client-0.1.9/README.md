# gapSolutions Client

**gapSolutions Client** is a Python library designed to interact with the gapSolutions API, enabling developers to seamlessly integrate gapSolutions features into their applications.

This client simplifies communication with the API, offering functions to interact with **measurement locations**, **organizations**, and **users**. Whether you are looking to fetch data, modify records, or perform deletion tasks, **gapSolutions Client** has got you covered.

---

## Features

- **Easy Authentication**: Use an API token for quick, secure access.
- **Measurement Locations**: Fetch, create, update, and delete measurement locations.
- **Organizations**: Manage organizations easily with simple API requests.
- **User Management**: Handle users' data with ease, including adding, deleting, and updating.
- **Automatic Handling of Responses**: Built-in error handling for clean and efficient workflows.

---

## Installation

You can install **gapSolutions Client** from PyPI using pip:

```bash
pip install gapSolutions_client
```

---

## Usage

### File Management Functions

```
from gapSolutions_client.file.file import ...
```

### 1. `file_list(auth_token, query_params=None)`
Retrieves a list of files from the API.

#### Parameters:
- `auth_token (str)`: API authentication token.
- `query_params (dict, optional)`: Query parameters to filter results.

#### Example Usage:
```python
response = file_list(auth_token, query_params={"all": "true", "lang": "en"})
print(response)
```

### 2. `file_create(auth_token, filename, file=None, status=None, note=None, folder_id=None, url=None, query_params=None)`
Creates a new file in the API.

#### Parameters:
- `auth_token (str)`: API authentication token.
- `filename (str)`: Name of the file.
- `file (optional)`: File data.
- `status (optional)`: File status.
- `note (optional)`: Additional notes.
- `folder_id (optional)`: Folder identifier.
- `url (optional)`: External file URL.
- `query_params (dict, optional)`: Additional query parameters.

#### Example Usage:
```python
response = file_create(auth_token, filename="document.pdf", status="active")
print(response)
```

### 3. `file_update(auth_token, file_id, filename, file=None, note=None, folder_id=None, url=None, query_params=None)`
Updates an existing file in the API.

#### Parameters:
- `auth_token (str)`: API authentication token.
- `file_id (str)`: ID of the file to update.
- `filename (str)`: Updated filename.
- `file (optional)`: New file data.
- `note (optional)`: Updated note.
- `folder_id (optional)`: Updated folder ID.
- `url (optional)`: Updated external URL.
- `query_params (dict, optional)`: Additional query parameters.

#### Example Usage:
```python
response = file_update(auth_token, file_id="12345", filename="updated_doc.pdf")
print(response)
```

### 4. `file_delete(auth_token, file_id, query_params=None)`
Deletes a file from the API.

#### Parameters:
- `auth_token (str)`: API authentication token.
- `file_id (str)`: ID of the file to delete.
- `query_params (dict, optional)`: Additional query parameters.

#### Example Usage:
```python
response = file_delete(auth_token, file_id="12345")
print(response)
```




## Account Management Functions

```
from gapSolutions_client.account.account import ...
```

#### 1. `account_selection(auth_token, query_params=None)`
Retrieves a list of accounts from the API.

**Parameters:**
- `auth_token (str)`: API authentication token used for authentication.
- `query_params (dict, optional)`: A dictionary containing query parameters for filtering the accounts list (e.g., `{"all": "true", "lang": "en"}`).

**Example Usage:**
```python
response = account_selection(auth_token, query_params={"all": "true", "lang": "en"})
print(response)
```



### Folder Management Functions

```
from gapSolutions_client.folder.folder import ...
```

#### 1. `folder_list(auth_token, query_params=None)`
Retrieves a list of folders from the API.

**Parameters:**
- `auth_token (str)`: API authentication token used for authentication.
- `query_params (dict, optional)`: A dictionary containing optional query parameters to filter folder retrieval results.

**Example Usage:**
```python
response = folder_list(auth_token)
print(response)
```

#### 2. `folder_create(auth_token, folder_id, folder_title, query_params=None)`
Creates a folder in the API.

**Parameters:**
- `auth_token (str)`: API authentication token used for authentication.
- `folder_id (str)`: A unique identifier for the folder.
- `folder_title (str)`: The name/title of the folder to be created.
- `query_params (dict, optional)`: A dictionary containing optional query parameters.

**Example Usage:**
```python
response = folder_create(auth_token, folder_id="123", folder_title="New Folder")
print(response)
```

#### 3. `folder_delete(auth_token, folder_id, query_params=None)`
Deletes a folder using the API.

**Parameters:**
- `auth_token (str)`: API authentication token used for authentication.
- `folder_id (str)`: The unique identifier of the folder to be deleted.
- `query_params (dict, optional)`: A dictionary containing optional query parameters.

**Example Usage:**
```python
response = folder_delete(auth_token, folder_id="123")
print(response)
```

#### 4. `folder_update(auth_token, folder_id, folder_data_text, query_params=None)`
Updates a folder using the API.

**Parameters:**
- `auth_token (str)`: API authentication token used for authentication.
- `folder_id (str)`: The unique identifier of the folder to be updated.
- `folder_data_text (str)`: The updated text or data for the folder.
- `query_params (dict, optional)`: A dictionary containing optional query parameters.

**Example Usage:**
```python
response = folder_update(auth_token, folder_id="123", folder_data_text="Updated Text")
print(response)
```

#### 5. `list_files_in_folder(auth_token, folder_id, query_params=None)`
Retrieves a list of files in a specified folder using the API.

**Parameters:**
- `auth_token (str)`: API authentication token used for authentication.
- `folder_id (str)`: The unique identifier of the folder whose files are being retrieved.
- `query_params (dict, optional)`: A dictionary containing optional query parameters (e.g., sorting options like `{"sort": "filename|asc"}`).

**Example Usage:**
```python
response = list_files_in_folder(auth_token, folder_id="123")
print(response)
```



