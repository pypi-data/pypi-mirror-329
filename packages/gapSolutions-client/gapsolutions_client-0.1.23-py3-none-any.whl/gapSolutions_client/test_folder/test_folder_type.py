import pytest
from datetime import datetime
from gapSolutions_client.folder.folder_type import Folder, from_int, from_str, from_datetime, from_union, from_list, from_none, folder_from_dict, folder_to_dict,from_bool


# Test utility functions

def test_from_int():
    assert from_int(10) == 10
    with pytest.raises(AssertionError):
        from_int("10")  # Should raise an assertion error

def test_from_str():
    assert from_str("hello") == "hello"
    with pytest.raises(AssertionError):
        from_str(10)  # Should raise an assertion error

def test_from_datetime():
    date_str = "2025-02-02T12:34:56"
    expected = datetime(2025, 2, 2, 12, 34, 56)
    assert from_datetime(date_str) == expected
    with pytest.raises(ValueError):
        from_datetime("invalid-date")  # Should raise a ValueError

def test_from_none():
    assert from_none(None) is None
    with pytest.raises(AssertionError):
        from_none("Not None")  # Should raise an assertion error

def test_from_union():
    # Union should try the first function (from_str) and succeed
    assert from_union([from_str, from_int], "test") == "test"
    # Union should try the second function (from_int) and succeed
    assert from_union([from_str, from_int], 10) == 10
    with pytest.raises(AssertionError):
        from_union([from_str, from_int], None)  # Should raise an assertion error

def test_from_list():
    assert from_list(from_int, [1, 2, 3]) == [1, 2, 3]
    with pytest.raises(AssertionError):
        from_list(from_int, "not a list")  # Should raise an assertion error

def test_from_bool():
    assert from_bool(True) is True
    assert from_bool(False) is False
    with pytest.raises(AssertionError):
        from_bool(10)  # Should raise an assertion error


# Test Folder class

def test_folder_from_dict():
    folder_data = {
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
    folder = Folder.from_dict(folder_data)

    # Test that the folder was created properly
    assert folder.id == 1
    assert folder.account_id == 2
    assert folder.title == "Test Folder"
    assert folder.created_at == datetime(2025, 2, 2, 12, 34, 56)
    assert folder.updated_at == datetime(2025, 2, 2, 12, 34, 56)
    assert folder.key == "folder-key"
    assert folder.parent_folder_id is None
    assert folder.all_childrens is None
    assert folder.children is None

def test_folder_to_dict():
    folder = Folder(
        id=1,
        account_id=2,
        title="Test Folder",
        permissions=None,
        created_at=datetime(2025, 2, 2, 12, 34, 56),
        updated_at=datetime(2025, 2, 2, 12, 34, 56),
        key="folder-key",
        parent_folder_id=None,
        all_childrens=[],
        children=[]
    )
    folder_dict = folder.to_dict()
    print("folder_dict",folder_dict)
    # Test that the dictionary matches expected values
    assert folder_dict["id"] == 1
    assert folder_dict["account_id"] == 2
    assert folder_dict["title"] == "Test Folder"
    assert folder_dict["created_at"] == "2025-02-02T12:34:56"
    assert folder_dict["updated_at"] == "2025-02-02T12:34:56"
    assert folder_dict["key"] == "folder-key"
    assert folder_dict["parent_folder_id"] is None
    assert folder_dict["all_childrens"] == []
    assert folder_dict["children"] == []


def test_folder_from_dict_list():
    folder_data = [
        {
            "id": 1,
            "account_id": 2,
            "title": "Test Folder 1",
            "permissions": None,
            "created_at": "2025-02-02T12:34:56",
            "updated_at": "2025-02-02T12:34:56",
            "key": "folder-key-1",
            "parent_folder_id": None,
            "all_childrens": None,
            "children": None
        },
        {
            "id": 2,
            "account_id": 3,
            "title": "Test Folder 2",
            "permissions": None,
            "created_at": "2025-02-02T12:34:56",
            "updated_at": "2025-02-02T12:34:56",
            "key": "folder-key-2",
            "parent_folder_id": None,
            "all_childrens": None,
            "children": None
        }
    ]
    folders = folder_from_dict(folder_data)

    # Test that the list of folders is parsed correctly
    assert len(folders) == 2
    assert folders[0].title == "Test Folder 1"
    assert folders[1].title == "Test Folder 2"


def test_folder_to_dict_list():
    folders = [
        Folder(
            id=1,
            account_id=2,
            title="Test Folder 1",
            permissions=None,
            created_at=datetime(2025, 2, 2, 12, 34, 56),
            updated_at=datetime(2025, 2, 2, 12, 34, 56),
            key="folder-key-1",
            parent_folder_id=None,
            all_childrens=None,
            children=None
        ),
        Folder(
            id=2,
            account_id=3,
            title="Test Folder 2",
            permissions=None,
            created_at=datetime(2025, 2, 2, 12, 34, 56),
            updated_at=datetime(2025, 2, 2, 12, 34, 56),
            key="folder-key-2",
            parent_folder_id=None,
            all_childrens=None,
            children=None
        )
    ]
    folder_dicts = folder_to_dict(folders)

    # Test that the list of folder dicts is correct
    assert len(folder_dicts) == 2
    assert folder_dicts[0]["title"] == "Test Folder 1"
    assert folder_dicts[1]["title"] == "Test Folder 2"


if __name__ == "__main__":
    pytest.main()
