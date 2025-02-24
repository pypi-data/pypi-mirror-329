"""
This module provides a `Folder` data model with serialization and deserialization capabilities.
"""
import dateutil.parser
from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, cast, Callable
from datetime import datetime


T = TypeVar("T")


def from_int(x: Any) -> int:
    """Ensures the value is an integer (not a boolean)."""
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    """Ensures the value is a string."""
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    """Ensures the value is None."""
    assert x is None
    return x


def from_datetime(x: Any) -> datetime:
    """Parses a string into a datetime object using dateutil.parser."""
    return dateutil.parser.parse(x)


def from_bool(x: Any) -> bool:
    """Ensures the value is a boolean."""
    assert isinstance(x, bool)
    return x


def from_union(fs, x):
    """Tries multiple conversion functions in sequence until one succeeds."""
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    """Converts a dataclass instance to a dictionary."""
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    """Converts a list of items using the provided function."""
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class AccountClass:
    id: int
    name: str
    merged_standard_descriptions: None

    @staticmethod
    def from_dict(obj: Any) -> 'AccountClass':
        """Creates an `AccountClass` instance from a dictionary."""
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        merged_standard_descriptions = from_none(obj.get("mergedStandardDescriptions"))
        return AccountClass(id, name, merged_standard_descriptions)

    def to_dict(self) -> dict:
        """Converts the `AccountClass` instance into a dictionary."""
        result: dict = {}
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        result["mergedStandardDescriptions"] = from_none(self.merged_standard_descriptions)
        return result


@dataclass
class Account:
    id: int
    account_id: int
    user_id: int
    type: str
    created_at: datetime
    updated_at: datetime
    favorite: bool
    role_id: int
    account: AccountClass
    last_log_in: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Account':
        """Creates an `Account` instance from a dictionary."""
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        account_id = from_int(obj.get("account_id"))
        user_id = from_int(obj.get("user_id"))
        type = from_str(obj.get("type"))
        created_at = from_datetime(obj.get("created_at"))
        updated_at = from_datetime(obj.get("updated_at"))
        favorite = from_bool(obj.get("favorite"))
        role_id = from_int(obj.get("role_id"))
        account = AccountClass.from_dict(obj.get("account"))
        last_log_in = from_union([from_none, from_datetime], obj.get("last_log_in"))
        return Account(id, account_id, user_id, type, created_at, updated_at, favorite, role_id, account, last_log_in)

    def to_dict(self) -> dict:
        """Converts the `Account` instance into a dictionary."""
        result: dict = {}
        result["id"] = from_int(self.id)
        result["account_id"] = from_int(self.account_id)
        result["user_id"] = from_int(self.user_id)
        result["type"] = from_str(self.type)
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        result["favorite"] = from_bool(self.favorite)
        result["role_id"] = from_int(self.role_id)
        result["account"] = to_class(AccountClass, self.account)
        result["last_log_in"] = from_union([from_none, lambda x: x.isoformat()], self.last_log_in)
        return result


def account_from_dict(s: Any) -> List[List[Account]]:
    """Parses a nested list of account dictionaries into a list of `Account` objects."""
    return from_list(lambda x: from_list(Account.from_dict, x), s)

def account_to_dict(x: List[List[Account]]) -> Any:
    """Converts a nested list of `Account` objects into a list of dictionaries."""
    return from_list(lambda x: from_list(lambda x: to_class(Account, x), x), x)
