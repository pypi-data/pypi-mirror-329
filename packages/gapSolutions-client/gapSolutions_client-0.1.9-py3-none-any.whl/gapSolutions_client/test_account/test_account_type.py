import pytest 
from datetime import datetime
from gapSolutions_client.account.account_type import (
    Account, AccountClass,
    from_int, from_str, from_datetime, from_union, from_list, from_none, from_bool,
    account_from_dict, account_to_dict
)

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
    assert from_union([from_str, from_int], "test") == "test"
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

# Test AccountClass model
def test_account_class():
    data = {"id": 1, "name": "Premium Account", "mergedStandardDescriptions": None}
    obj = AccountClass.from_dict(data)
    assert obj.id == 1
    assert obj.name == "Premium Account"
    assert obj.to_dict() == data

# Test Account model
def test_account_from_dict():
    data = {
        "id": 1,
        "account_id": 100,
        "user_id": 200,
        "type": "admin",
        "created_at": "2025-02-02T12:34:56",
        "updated_at": "2025-02-02T12:34:56",
        "favorite": True,
        "role_id": 3,
        'last_log_in': None,
        "account": {"id": 1, "name": "Business Account", "mergedStandardDescriptions": None}
    }
    account = Account.from_dict(data)
    assert account.id == 1
    assert account.account_id == 100
    assert account.type == "admin"
    assert account.to_dict() == data

def test_account_to_dict():
    account = Account(
        id=1,
        account_id=100,
        user_id=200,
        type="admin",
        created_at=datetime(2025, 2, 2, 12, 34, 56),
        updated_at=datetime(2025, 2, 2, 12, 34, 56),
        favorite=True,
        role_id=3,
        account=AccountClass(id=1, name="Business Account", merged_standard_descriptions=None)
    )
    account_dict = account.to_dict()
    assert account_dict["id"] == 1
    assert account_dict["account_id"] == 100
    assert account_dict["type"] == "admin"

def test_account_from_dict_list():
    account_data = [
        [
            {
                "id": 1,
                "account_id": 2,
                "user_id": 3,
                "type": "user",
                "created_at": "2025-02-02T12:34:56",
                "updated_at": "2025-02-02T12:34:56",
                "favorite": False,
                "role_id": 4,
                "account": {"id": 1, "name": "Personal Account", "mergedStandardDescriptions": None}
            }
        ]
    ]
    accounts = account_from_dict(account_data)
    assert len(accounts) == 1
    assert len(accounts[0]) == 1
    assert accounts[0][0].type == "user"

def test_account_to_dict_list():
    accounts = [
        [
            Account(
                id=1,
                account_id=2,
                user_id=3,
                type="user",
                created_at=datetime(2025, 2, 2, 12, 34, 56),
                updated_at=datetime(2025, 2, 2, 12, 34, 56),
                favorite=False,
                role_id=4,
                account=AccountClass(id=1, name="Personal Account", merged_standard_descriptions=None)
            )
        ]
    ]
    account_dicts = account_to_dict(accounts)
    assert len(account_dicts) == 1
    assert len(account_dicts[0]) == 1
    assert account_dicts[0][0]["type"] == "user"

if __name__ == "__main__":
    pytest.main()
