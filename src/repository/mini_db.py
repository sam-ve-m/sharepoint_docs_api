import json
import os


class MiniDB:
    def __init__(self, database_path: str):
        self._db_path = database_path
        if not self._db_path:
            return
        if not os.path.exists(self._db_path):
            with open(self._db_path, "w") as _file:
                _file.write("{}")

    def _read(self) -> dict:
        if not self._db_path:
            return {}
        with open(self._db_path, "r") as file:
            full_db = json.loads(file.read())
            return full_db

    def get(self, key: str, default=None) -> any:
        return self._read().get(key, default)

    def set(self, key: str, value):
        if not self._db_path:
            return
        full_db = self._read()
        full_db[key] = value
        with open(self._db_path, "w") as file:
            json.dump(full_db, file)
