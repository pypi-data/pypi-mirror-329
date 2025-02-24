import unittest
from datetime import datetime
# from file.file_type import File, Version, Link, Filename, MIMEType, Status, Notes 
from ..file.file_type import File, Version, Link, Filename, MIMEType, Status, Notes

class TestFileClass(unittest.TestCase):

    def setUp(self):
        """Set up test data before each test"""
        self.file_data = {
            "id": 1,
            "account_id": 101,
            "filename": "linkedIn2",
            "read_note": None,
            "path": "/files/sample.jpg",
            "mime_type": "image/jpeg",
            "size": 2048,
            "created_at": "2023-01-01T12:00:00Z",
            "updated_at": "2023-01-02T12:00:00Z",
            "category_id": None,
            "fileable_id": None,
            "fileable_type": None,
            "additional_params": None,
            "force_download": 0,
            "category": None,
            "latest_version": {
                "id": 1,
                "file_id": 1,
                "version": 1,
                "status": "approvalflow_disabled",
                "read_note": None,
                "filename": "linkedIn2",
                "path": "/files/sample_v1.jpg",
                "mime_type": "image/jpeg",
                "size": 2048,
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-02T12:00:00Z",
                "read_percent": None,
                "log_entry": None,
                "text": None,
                "readers": None
            },
            "latest_approved_version": {
                "id": 1,
                "file_id": 1,
                "version": 1,
                "status": "approvalflow_disabled",
                "read_note": None,
                "filename": "linkedIn2",
                "path": "/files/sample_v1.jpg",
                "mime_type": "image/jpeg",
                "size": 2048,
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-02T12:00:00Z",
                "read_percent": None,
                "log_entry": None,
                "text": None,
                "readers": None
            },
            "versions": [],
            "inspections": [],
            "notes": None,
            "link": {
                "id": 1,
                "file_id": 1,
                "url": "https://example.com/file",
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-02T12:00:00Z"
            }
        }

    def test_from_dict(self):
        """Test conversion from dictionary to File object"""
        file_obj = File.from_dict(self.file_data)
        self.assertEqual(file_obj.id, 1)
        self.assertEqual(file_obj.account_id, 101)
        self.assertEqual(file_obj.filename, Filename.LINKED_IN2)
        self.assertEqual(file_obj.mime_type, MIMEType.IMAGE_JPEG)
        self.assertEqual(file_obj.size, 2048)
        self.assertEqual(file_obj.path, "/files/sample.jpg")
        self.assertIsInstance(file_obj.created_at, datetime)
        self.assertIsInstance(file_obj.updated_at, datetime)

    # def test_to_dict(self):
    #     """Test conversion from File object to dictionary"""
    #     file_obj = File.from_dict(self.file_data)
    #     file_dict = file_obj.to_dict()
    #     self.assertEqual(file_dict["id"], self.file_data["id"])
    #     self.assertEqual(file_dict["filename"], self.file_data["filename"])
    #     self.assertEqual(file_dict["mime_type"], self.file_data["mime_type"])
    #     self.assertEqual(file_dict["size"], self.file_data["size"])
    #     self.assertEqual(file_dict["path"], self.file_data["path"])
    #     self.assertEqual(file_dict["created_at"], self.file_data["created_at"])

    def test_round_trip_serialization(self):
        """Test that serializing and then deserializing produces the same data"""
        file_obj = File.from_dict(self.file_data)
        file_dict = file_obj.to_dict()
        new_file_obj = File.from_dict(file_dict)
        self.assertEqual(new_file_obj, file_obj)


if __name__ == "__main__":
    unittest.main()
