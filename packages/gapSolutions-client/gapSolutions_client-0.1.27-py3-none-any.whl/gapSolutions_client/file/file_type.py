import dateutil.parser
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()





class MIMEType(Enum):
    IMAGE_JPEG = "image/jpeg"
    URL = "url"


class Status(Enum):
    APPROVALFLOW_DISABLED = "approvalflow_disabled"


class Notes(Enum):
    AAA = "aaa"


@dataclass
class Version:
    id: int
    file_id: int
    version: int
    status: Status
    read_note: None
    filename: str
    path: str
    mime_type: MIMEType
    size: int
    created_at: datetime
    updated_at: datetime
    read_percent: None
    log_entry: None  # Move log_entry above optional fields
    text: Optional[Notes] = None
    readers: Optional[List[Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Version':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        file_id = from_int(obj.get("file_id"))
        version = from_int(obj.get("version"))
        status = Status(obj.get("status"))
        read_note = from_none(obj.get("read_note"))
        filename = obj.get("filename")
        path = from_str(obj.get("path"))
        mime_type = MIMEType(obj.get("mime_type"))
        size = from_int(obj.get("size"))
        created_at = from_datetime(obj.get("created_at"))
        updated_at = from_datetime(obj.get("updated_at"))
        read_percent = from_none(obj.get("read_percent"))
        text = from_union([from_none, Notes], obj.get("text"))
        log_entry = from_none(obj.get("log_entry"))
        readers = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("readers"))
        return Version(id, file_id, version, status, read_note, filename, path, mime_type, size, created_at, updated_at, read_percent, text, log_entry, readers)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["file_id"] = from_int(self.file_id)
        result["version"] = from_int(self.version)
        result["status"] = to_enum(Status, self.status)
        result["read_note"] = from_none(self.read_note)
        result["filename"] = from_str(self.filename)
        result["path"] = from_str(self.path)
        result["mime_type"] = to_enum(MIMEType, self.mime_type)
        result["size"] = from_int(self.size)
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        result["read_percent"] = from_none(self.read_percent)
        result["text"] = from_union([from_none, lambda x: to_enum(Notes, x)], self.text)
        if self.log_entry is not None:
            result["log_entry"] = from_none(self.log_entry)
        if self.readers is not None:
            result["readers"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.readers)
        return result


@dataclass
class Link:
    id: int
    file_id: int
    url: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_dict(obj: Any) -> 'Link':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        file_id = from_int(obj.get("file_id"))
        url = from_str(obj.get("url"))
        created_at = from_datetime(obj.get("created_at"))
        updated_at = from_datetime(obj.get("updated_at"))
        return Link(id, file_id, url, created_at, updated_at)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["file_id"] = from_int(self.file_id)
        result["url"] = from_str(self.url)
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        return result


@dataclass
class File:
    id: int
    account_id: int
    filename: str
    read_note: None
    path: str
    mime_type: MIMEType
    size: int
    created_at: datetime
    updated_at: datetime
    category_id: None
    fileable_id: None
    fileable_type: None
    additional_params: None
    force_download: int
    category: None
    latest_version: Version
    latest_approved_version: Version
    versions: List[Version]
    inspections: List[Any]
    notes: Optional[Notes] = None
    link: Optional[Link] = None

    @staticmethod
    def from_dict(obj: Any) -> 'File':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        account_id = from_int(obj.get("account_id"))
        filename = (obj.get("filename"))
        read_note = from_none(obj.get("read_note"))
        path = from_str(obj.get("path"))
        mime_type = MIMEType(obj.get("mime_type"))
        size = from_int(obj.get("size"))
        created_at = from_datetime(obj.get("created_at"))
        updated_at = from_datetime(obj.get("updated_at"))
        category_id = from_none(obj.get("category_id"))
        fileable_id = from_none(obj.get("fileable_id"))
        fileable_type = from_none(obj.get("fileable_type"))
        additional_params = from_none(obj.get("additional_params"))
        force_download = from_int(obj.get("force_download"))
        category = from_none(obj.get("category"))
        latest_version = Version.from_dict(obj.get("latest_version"))
        latest_approved_version = Version.from_dict(obj.get("latest_approved_version"))
        versions = from_list(Version.from_dict, obj.get("versions"))
        inspections = from_list(lambda x: x, obj.get("inspections"))
        notes = from_union([from_none, Notes], obj.get("notes"))
        link = from_union([from_none, Link.from_dict], obj.get("link"))
        return File(id, account_id, filename, read_note, path, mime_type, size, created_at, updated_at, category_id, fileable_id, fileable_type, additional_params, force_download, category, latest_version, latest_approved_version, versions, inspections, notes, link)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["account_id"] = from_int(self.account_id)
        result["filename"] = to_enum(self.filename)
        result["read_note"] = from_none(self.read_note)
        result["path"] = from_str(self.path)
        result["mime_type"] = to_enum(MIMEType, self.mime_type)
        result["size"] = from_int(self.size)
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        result["category_id"] = from_none(self.category_id)
        result["fileable_id"] = from_none(self.fileable_id)
        result["fileable_type"] = from_none(self.fileable_type)
        result["additional_params"] = from_none(self.additional_params)
        result["force_download"] = from_int(self.force_download)
        result["category"] = from_none(self.category)
        result["latest_version"] = to_class(Version, self.latest_version)
        result["latest_approved_version"] = to_class(Version, self.latest_approved_version)
        result["versions"] = from_list(lambda x: to_class(Version, x), self.versions)
        result["inspections"] = from_list(lambda x: x, self.inspections)
        result["notes"] = from_union([from_none, lambda x: to_enum(Notes, x)], self.notes)
        result["link"] = from_union([from_none, lambda x: to_class(Link, x)], self.link)
        return result


def file_from_dict(s: Any) -> List[File]:
    return from_list(File.from_dict, s)


def file_to_dict(x: List[File]) -> Any:
    return from_list(lambda x: to_class(File, x), x)
