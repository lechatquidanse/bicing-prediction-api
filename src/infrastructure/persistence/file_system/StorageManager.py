"""
Manage storage folder creation and clean
"""
import os


class StorageManager:
    @staticmethod
    def create_storage_location(path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)

    @staticmethod
    def truncate_storage_location(path):
        for the_file in os.listdir(path):
            file_path = os.path.join(path, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
