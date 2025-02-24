"""
This module provides a `Folder` data model with serialization and deserialization capabilities.
"""
import dateutil.parser
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Union, Any, TypeVar, Callable, Type, cast

T = TypeVar("T")


def from_int(x: Any) -> int:
    """
    Converts a value to an integer if it is a valid integer.
    Raises an assertion error if the input is not an integer.
    """
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    """
    Converts a value to a string if it is a valid string.
    Raises an assertion error if the input is not a string.
    """
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    """
    Ensures that the value is None.
    Raises an assertion error if the input is not None.
    """
    assert x is None
    return x


def from_datetime(x: Any) -> datetime:
    """
    Parses a string into a datetime object using dateutil.parser.
    """
    return dateutil.parser.parse(x)


def from_union(fs, x):
    """
    Tries multiple conversion functions in sequence until one succeeds.
    Raises an assertion error if none of the functions work.
    """
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    """
    Converts a list of values using a provided conversion function.
    Raises an assertion error if the input is not a list.
    """
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    """
    Ensures that the input is a boolean.
    Raises an assertion error if the input is not a boolean.
    """
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    """
    Converts an instance of a class to a dictionary by calling its to_dict method.
    """
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Folder:
    """
    Represents a folder with various attributes including ID, account ID,
    title, permissions, timestamps, and nested folder structures.
    """
    id: int
    account_id: int
    title: str
    permissions: None
    created_at: datetime
    updated_at: datetime
    key: Optional[str] = None
    parent_folder_id: Optional[int] = None
    all_childrens: Optional[Union[List['Folder'], bool]] = None
    children: Optional[List['Folder']] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Folder':
        """
        Creates a Folder object from a dictionary.
        Raises an assertion error if the input is not a dictionary.
        """
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        account_id = from_int(int(obj.get("account_id")))
        title = from_str(obj.get("title"))
        permissions = from_none(obj.get("permissions"))
        created_at = from_datetime(obj.get("created_at"))
        updated_at = from_datetime(obj.get("updated_at"))
        key = from_union([from_str, from_none], obj.get("key"))
        parent_folder_id = from_union([from_none, from_int], obj.get("parent_folder_id"))
        all_childrens = from_union([lambda x: from_list(Folder.from_dict, x), from_bool, from_none], obj.get("all_childrens"))
        children = from_union([lambda x: from_list(Folder.from_dict, x), from_none], obj.get("children"))
        return Folder(id, account_id, title, permissions, created_at, updated_at, key, parent_folder_id, all_childrens, children)

    def to_dict(self) -> dict:
        """
        Converts the Folder object into a dictionary.
        """
        result: dict = {}
        result["id"] = from_int(self.id)
        result["account_id"] = from_int(self.account_id)
        result["title"] = from_str(self.title)
        result["permissions"] = from_none(self.permissions)
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        result["key"] = from_str(self.key)
        result["parent_folder_id"] = from_union([from_none, from_int], self.parent_folder_id)
        if self.all_childrens is not None:
            result["all_childrens"] = from_union([lambda x: from_list(lambda x: to_class(Folder, x), x), from_bool, from_none], self.all_childrens)
        if self.children is not None:
            result["children"] = from_union([lambda x: from_list(lambda x: to_class(Folder, x), x), from_none], self.children)
        return result


def folder_from_dict(s: Any) -> List[Folder]:
    """
    Converts a dictionary list into a list of Folder objects.
    """
    return from_list(Folder.from_dict, s)


def folder_to_dict(x: List[Folder]) -> Any:
    """
    Converts a list of Folder objects into a dictionary list.
    """
    return from_list(lambda x: to_class(Folder, x), x)
