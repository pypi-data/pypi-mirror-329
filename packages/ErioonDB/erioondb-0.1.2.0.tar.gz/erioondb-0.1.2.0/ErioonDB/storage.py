import os
import json
import threading
import time
import logging
import uuid
import shelve
from collections import defaultdict
from contextlib import contextmanager
import pickle

# ReadWriteLock to handle concurrent read/write
class ReadWriteLock:
    def __init__(self):
        self._readers = 0
        self._writer = False
        self._condition = threading.Condition()

    def acquire_read(self):
        with self._condition:
            while self._writer:
                self._condition.wait()
            self._readers += 1

    def release_read(self):
        with self._condition:
            self._readers -= 1
            if self._readers == 0:
                self._condition.notify_all()

    def acquire_write(self):
        with self._condition:
            while self._writer or self._readers > 0:
                self._condition.wait()
            self._writer = True

    def release_write(self):
        with self._condition:
            self._writer = False
            self._condition.notify_all()


class ErioonClient:
    def __init__(self):
        self.data = {}  # Store data in memory
        self.indexes = defaultdict(set)  # In-memory indexes
        self.lock = threading.Lock()
        self.rw_lock = ReadWriteLock()
        self.transaction_buffer = []
        self.transaction_lock = threading.Lock()

        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def __getitem__(self, db_name):
        """Allows access to databases by name."""
        if db_name not in self.data:
            self.data[db_name] = Database(self, db_name)
        return self.data[db_name]



class Database:
    def __init__(self, client, db_name):
        """Initialize the Database object."""
        self.client = client
        self.db_name = db_name
        self.storage_file = os.path.abspath(f"./db/{db_name}/{db_name}.db")

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        self.data = {}

        self._load_data()
        self._initialize_default_collections()

    def _load_data(self):
        """Load data from shelve storage."""
        try:
            with shelve.open(self.storage_file, "c") as db:
                self.data = dict(db)
                self.logger.info(f"Data loaded from {self.storage_file}.")
        except Exception as e:
            self.logger.error(f"Error loading data: {e}. Starting with an empty database.")
            self.data = {}

    def _save_data(self):
        """Save data to shelve storage."""
        try:
            with shelve.open(self.storage_file, "c") as db:
                db.update(self.data)
            self.logger.info(f"Data saved to {self.storage_file}.")
        except Exception as e:
            self.logger.error(f"Error saving data: {e}.")

    def __getitem__(self, collection_name):
        """Allow access to collections by name."""
        if collection_name == self.db_name:
            raise ValueError(f"The database name '{self.db_name}' cannot be used as a collection.")

        if collection_name not in self.data:
            self.data[collection_name] = Collection(self.client, self.db_name, collection_name)
        return self.data[collection_name]

    def _initialize_default_collections(self):
        """Ensure that 'user' and 'config' collections are created."""
        collections_to_initialize = ["user", "config"]

        for collection_name in collections_to_initialize:
            if collection_name not in self.data:
                self.data[collection_name] = Collection(self.client, self.db_name, collection_name)
                self.logger.info(f"Collection '{collection_name}' created in database '{self.db_name}'.")
                if collection_name == "user":
                    self.data[collection_name].insert({"default_user": "admin"})
                elif collection_name == "config":
                    self.data[collection_name].insert({"default_config": "enabled"})

        self._save_data()


class Collection:
    def __init__(self, client, db_name, collection_name):
        self.client = client
        self.db_name = db_name
        self.collection_name = collection_name

        self.storage_file = os.path.abspath(f"./db/{db_name}/{collection_name}.db")
        self.index_file = os.path.abspath(f"./db/{db_name}/{collection_name}_indexes.json")
        self.wal_file = os.path.abspath(f"./db/{db_name}/{collection_name}_wal.json")

        self.data = {}
        self.indexes = defaultdict(lambda: defaultdict(set))
        self.transaction_buffer = []

        self.rw_lock = ReadWriteLock()
        self.logger = logging.getLogger(__name__)

        self._load_data()
        self._load_indexes()
        self._load_wal()

    def _load_data(self):
        """Load persistent data safely with read lock."""
        self.rw_lock.acquire_read()
        try:
            if os.path.exists(self.storage_file):
                try:
                    with shelve.open(self.storage_file, "r") as db:
                        self.data = {k: v for k, v in db.items()}  # Properly read stored data
                        self.logger.info(f"Data loaded from {self.storage_file}.")
                except Exception as e:
                    self.logger.error(f"Error loading data from {self.storage_file}: {e}.")
                    self.data = {}
            else:
                self.logger.warning(f"{self.storage_file} not found, starting with an empty database.")
                self.data = {}
        finally:
            self.rw_lock.release_read()


    def _save_data(self):
        """Save the database data, ensuring only serializable objects are stored."""
        try:
            safe_data = {k: v for k, v in self.data.items() if isinstance(v, dict)}  # Only save valid data

            with shelve.open(self.storage_file, "c") as db:
                db.clear()  # Clear old data to prevent stale entries
                db.update(safe_data)  # Save only serializable data

            self.logger.info(f"Data saved to {self.storage_file}.")
        except Exception as e:
            self.logger.error(f"Error saving data: {e}")




    def insert(self, document):
        """Insert a document into the collection and save."""
        if "_id" not in document:
            document["_id"] = str(uuid.uuid4())

        self.data[document["_id"]] = document
        self._save_data()

        self.logger.info(f"Inserted into {self.collection_name}: {document}")
        print(f"Inserted into {self.collection_name}: {document}")


    def _load_indexes(self):
        """Load indexes from persistent storage."""
        if os.path.exists(self.index_file):
            if os.path.getsize(self.index_file) == 0:
                self.indexes = defaultdict(lambda: defaultdict(set))
                return
            try:
                with open(self.index_file, "r") as file:
                    self.indexes = json.load(file)
            except (json.JSONDecodeError, ValueError):
                self.logger.error(f"Error loading indexes from {self.index_file}, resetting indexes.")
                self.indexes = defaultdict(lambda: defaultdict(set))

    def _save_indexes(self):
        """Save indexes to persistent storage."""
        with open(self.index_file, "w") as file:
            json.dump(self.indexes, file, indent=4)
            self.logger.info(f"Indexes saved to {self.index_file}.")

    def _load_wal(self):
        """Load the write-ahead log (WAL) to recover uncommitted transactions."""
        if os.path.exists(self.wal_file):
            with open(self.wal_file, "r") as file:
                wal_entries = json.load(file)
                for entry in wal_entries:
                    self._apply_log_entry(entry)

    def _save_wal(self):
        """Persist the write-ahead log."""
        with open(self.wal_file, "w") as file:
            json.dump(self.transaction_buffer, file, indent=4)
            self.logger.info(f"WAL saved to {self.wal_file}.")

    def _apply_log_entry(self, entry):
        """Apply a WAL log entry to recover lost data."""
        op, collection, key, value = entry["operation"], entry["collection"], entry["key"], entry.get("value")
        if op == "INSERT":
            self.data.setdefault(collection, {})[key] = value
        elif op == "UPDATE":
            self.data[collection][key] = value
        elif op == "DELETE":
            del self.data[collection][key]

    def _write_wal(self, operation, collection, key, value=None):
        """Enqueue a WAL log entry for asynchronous writing."""
        timestamp = time.time()
        log_entry = {
            "operation": operation,
            "collection": collection,
            "key": key,
            "value": value,
            "timestamp": timestamp,
        }
        self.transaction_buffer.append(log_entry)

    @contextmanager
    def transaction(self):
        """Context manager for transactions with rollback support."""
        try:
            self.transaction_buffer = []
            yield self
            self._commit_transaction()
        except Exception as e:
            self.logger.error(f"Transaction failed: {e}")
            self._rollback_transaction()
            raise

    def _commit_transaction(self):
        """Commit the transaction and apply changes to persistent storage."""
        try:
            for op, collection, key, value in self.transaction_buffer:
                if op == "INSERT":
                    self.data.setdefault(collection, {})[key] = value
                elif op == "UPDATE":
                    self.data[collection][key] = value
                elif op == "DELETE":
                    del self.data[collection][key]

            self._save_data()
            self._save_wal()
            self.transaction_buffer = []
            self.logger.info("Transaction committed successfully.")
        except Exception as e:
            self.logger.error(f"Error during transaction commit: {e}. Rolling back.")
            self._rollback_transaction()

    def _rollback_transaction(self):
        """Rollback the transaction."""
        self.logger.info("Transaction rolled back.")
        self.transaction_buffer = []

    def insert(self, document):
        """Insert a document into the collection and force-save the data."""
        if "_id" not in document:
            document["_id"] = str(uuid.uuid4())  # Generate an _id if not present
    
        self.data[document["_id"]] = document  # Store in memory
        self._save_data()  # 🔥 Force-save to disk
        
        self.logger.info(f"Inserted into {self.collection_name}: {document}")
        print(f"Inserted into {self.collection_name}: {document}")  # Debugging
    

    def update(self, key, document):
        """Update an existing document."""
        key = str(key)
        self.rw_lock.acquire_write()
        try:
            if key not in self.data:
                raise ValueError("Document not found.")
            self.data[key].update(document)
            self._save_data()
            self.logger.info(f"Document with key {key} updated.")
        finally:
            self.rw_lock.release_write()

    def delete(self, key):
        """Delete a document."""
        key = str(key)
        self.rw_lock.acquire_write()
        try:
            if key not in self.data:
                raise ValueError("Document not found.")
            del self.data[key]
            self._save_data()
            self.logger.info(f"Document with key {key} deleted.")
        finally:
            self.rw_lock.release_write()

    def find(self, query=None):
        """Find documents matching the query."""
        self.rw_lock.acquire_read()
        try:
            if query is None:
                print(f"All data: {self.data}")
                return list(self.data.values())

            results = []
            for key, value in self.data.items():
                if all(value.get(field) == field_value for field, field_value in query.items()):
                    results.append(value)

            return results
        finally:
            self.rw_lock.release_read()

    def get_all(self):
        try:
            with shelve.open(self.storage_file) as db:
                return list(db.values())  # Or adjust based on your data structure
        except Exception as e:
            print("Error loading data:", e)
            return []
