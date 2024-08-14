import json
import os


class MiniDB:
    def __init__(self, database_path: str, collection: str):
        if database_path[-5:] != ".json":
            database_path += ".json"
        self._db_path = database_path
        self.collection = collection
        if not os.path.exists(self._db_path):
            os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
            with open(self._db_path, "w") as _file:
                _file.write("{}")

    def _read(self) -> dict:
        with open(self._db_path, "r") as file:
            full_db = json.loads(file.read())
            return full_db

    def get(self, key: str, default=None) -> any:
        return self._read().get(self.collection, {}).get(key, default)

    def set(self, key: str, value):
        full_db = self._read()
        full_collection = full_db.get(self.collection, {})
        full_collection[key] = value
        full_db[self.collection] = full_collection
        with open(self._db_path, "w") as file:
            json.dump(full_db, file)
