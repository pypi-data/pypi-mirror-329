import os
import json
import threading
import time
import logging
from collections import defaultdict
from contextlib import contextmanager
import uuid
import shelve
import dbm.dumb
import shutil
import queue

class ReadWriteLock:
    def __init__(self):
        self._readers = 0
        self._writer = False
        self._condition = threading.Condition()

    def acquire_read(self):
        """Acquire a read lock. Multiple readers are allowed."""
        with self._condition:
            while self._writer:
                self._condition.wait()
            self._readers += 1

    def release_read(self):
        """Release a read lock."""
        with self._condition:
            self._readers -= 1
            if self._readers == 0:
                self._condition.notify_all()

    def acquire_write(self):
        """Acquire a write lock. Only one writer is allowed."""
        with self._condition:
            while self._writer or self._readers > 0: 
                self._condition.wait()
            self._writer = True

    def release_write(self):
        """Release a write lock."""
        with self._condition:
            self._writer = False
            self._condition.notify_all()


class ErioonClient:
    def __init__(self, storage_file="store.db", wal_file="store.wal", index_file="indexes.idx"):
        self.wal_queue = queue.Queue()
        threading.Thread(target=self._wal_writer, daemon=True).start()
        self.storage_file = storage_file
        self.wal_file = wal_file  # Ensure wal_file is set properly
        self.index_file = index_file
        self.data = {}
        self.indexes = defaultdict(set)
        self.write_ahead_log = []
        self.lock = threading.Lock()
        self.transaction_buffer = []
        self.transaction_lock = threading.Lock()
        self.rw_lock = ReadWriteLock()

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        self._load_data()
        self._load_wal()
        self._load_indexes()

    def _save_data(self):
        """Thread-safe persistent storage using shelve with write lock."""
        self.rw_lock.acquire_write()
        try:
            with shelve.open(self.storage_file, "c") as db:
                db.update(self.data)
        finally:
            self.rw_lock.release_write()

    def _load_data(self):
        """Load persistent data safely with read lock."""
        self.rw_lock.acquire_read()
        try:
            if os.path.exists(self.storage_file):
                try:
                    with shelve.open(self.storage_file, "r") as db:
                        self.data = dict(db)
                except dbm.error as e:
                    self.logger.error(f"Database error while loading: {e}. Corrupted database file detected. Resetting data.")
                    self.data = {}
                except PermissionError as e:
                    self.logger.error(f"Permission error: {e}. Unable to read the database file.")
                    self.data = {}
                except Exception as e:
                    self.logger.error(f"Unexpected error while loading the database: {e}. Resetting data.")
                    self.data = {}
            else:
                self.data = {}
        finally:
            self.rw_lock.release_read()

    def _load_wal(self):
        """Loads the write-ahead log (WAL) to recover uncommitted transactions."""
        if os.path.exists(self.wal_file):
            with open(self.wal_file, "r") as file:
                self.write_ahead_log = json.load(file)
                for entry in self.write_ahead_log:
                    self._apply_log_entry(entry)

    def _save_wal(self):
        """Persists the write-ahead log."""
        with open(self.wal_file, "w") as file:
            json.dump(self.write_ahead_log, file, indent=4)

    def _apply_log_entry(self, entry):
        """Applies a WAL log entry to recover lost data."""
        op, collection, key, value = entry["operation"], entry["collection"], entry["key"], entry.get("value")
        if op == "INSERT":
            self.data.setdefault(collection, {})[key] = value
        elif op == "UPDATE":
            self.data[collection][key] = value
        elif op == "DELETE":
            del self.data[collection][key]

    def _write_wal(self, operation, collection, key, value=None):
        """Enqueues a WAL log entry for asynchronous writing."""
        timestamp = time.time()
        log_entry = {"operation": operation, "collection": collection, "key": key, "value": value, "timestamp": timestamp}
        self.wal_queue.put(log_entry)

    def _wal_writer(self):
        """Efficient WAL writer thread."""
        with open(self.wal_file, "a", buffering=1) as file:
            while True:
                try:
                    entry = self.wal_queue.get(timeout=5)
                    file.write(json.dumps(entry) + "\n")
                    file.flush()
                    os.fsync(file.fileno()) 
                except queue.Empty:
                    continue 

    def _load_indexes(self):
        """Fix: Handle empty or corrupted index file."""
        if os.path.exists(self.index_file):
            if os.path.getsize(self.index_file) == 0: 
                self.indexes = defaultdict(lambda: defaultdict(set))
                return

            try:
                with open(self.index_file, "r") as file:
                    raw_indexes = json.load(file)
                    self.indexes = defaultdict(lambda: defaultdict(set))
                    for field, values in raw_indexes.items():
                        for value, keys in values.items():
                            self.indexes[field][value] = set(keys) 
            except (json.JSONDecodeError, ValueError):
                self.logger.error("Corrupted index file detected. Resetting indexes.")
                self.indexes = defaultdict(lambda: defaultdict(set))

    def _save_indexes(self):
        """Fix: Convert sets to lists before saving JSON."""
        with open(self.index_file, "w") as file:
            json.dump({field: {value: list(keys) for value, keys in values.items()} for field, values in self.indexes.items()}, file, indent=4)

    def _update_indexes(self, collection, key, value, operation):
        """Manages indexing on data changes."""
        try:
            if operation in ["INSERT", "UPDATE"]:
                for field, field_value in value.items():
                    if field not in self.indexes:
                        self.indexes[field] = defaultdict(set) 
                    self.indexes[field][field_value].add(key) 
    
            elif operation == "DELETE":
                if key in self.data[collection]:  
                    for field, field_value in self.data[collection][key].items():
                        if field in self.indexes and field_value in self.indexes[field]:
                            self.indexes[field][field_value].discard(key)
                            if not self.indexes[field][field_value]: 
                                del self.indexes[field][field_value]
    
            self._save_indexes()
        
        except KeyError as e:
            self.logger.error(f"Key error while updating index for key {key}: {e}.")
        except Exception as e:
            self.logger.error(f"Unexpected error while updating indexes: {e}.")

    @contextmanager
    def transaction(self):
        """Context manager for transactions with rollback support."""
        with self.transaction_lock:
            try:
                self.transaction_buffer = []
                yield self
                self._commit_transaction()
            except Exception as e:
                self.logger.error(f"Transaction failed: {e}")
                self._rollback_transaction()
                raise

    def _commit_transaction(self):
        """Fully atomic transaction commit."""
        with self.lock:
            try:
                temp_buffer = [] 
                for op, collection, key, value in self.transaction_buffer:
                    temp_buffer.append((op, collection, key, value))  

                for op, collection, key, value in temp_buffer:
                    if op == "INSERT":
                        self.data.setdefault(collection, {})[key] = value
                    elif op == "UPDATE":
                        self.data[collection][key] = value
                    elif op == "DELETE":
                        del self.data[collection][key]

                self._save_data()
                self.write_ahead_log.clear()  
                self.transaction_buffer = [] 
                self.logger.info("Transaction committed successfully.")

            except KeyError as e:
                self.logger.error(f"KeyError during transaction commit: {e}. Rolling back.")
                self._rollback_transaction()
                raise 
            except PermissionError as e:
                self.logger.error(f"Permission error during transaction commit: {e}. Rolling back.")
                self._rollback_transaction()
                raise
            except Exception as e:
                self.logger.error(f"Unexpected error during transaction commit: {e}. Rolling back.")
                self._rollback_transaction()
                raise

    def _rollback_transaction(self):
        """Rolls back a transaction."""
        self.logger.info("Transaction rolled back due to an error.")
        self.transaction_buffer = [] 

    def insert(self, collection, document):
        """Inserts a document into a collection with an auto-generated _id."""
        if "_id" not in document: 
            document["_id"] = str(uuid.uuid4()) 

        key = document["_id"]
        
        self.rw_lock.acquire_write()
        try:
            if key in self.data.get(collection, {}):
                self.logger.error(f"Attempted to insert duplicate key '{key}' into collection '{collection}'.")
                raise KeyError(f"Key '{key}' already exists in collection '{collection}'.")
            self.transaction_buffer.append(("INSERT", collection, key, document))
            self.logger.info(f"Queued INSERT {key} in collection {collection}.")
        finally:
            self.rw_lock.release_write()

    def update(self, collection, key, document):
        """Updates an existing document."""
        key = str(key)
        
        self.rw_lock.acquire_write()
        try:
            if key not in self.data.get(collection, {}):
                raise KeyError(f"Key '{key}' not found.")
            self.transaction_buffer.append(("UPDATE", collection, key, document))
            self.logger.info(f"Queued UPDATE {key} in collection {collection}.")
        finally:
            self.rw_lock.release_write()

    def delete(self, collection, key):
        """Deletes a document from a collection."""
        key = str(key)
        
        self.rw_lock.acquire_write()
        try:
            if key not in self.data.get(collection, {}):
                raise KeyError(f"Key '{key}' not found.")
            self.transaction_buffer.append(("DELETE", collection, key, None))
            self.logger.info(f"Queued DELETE {key} in collection {collection}.")
        finally:
            self.rw_lock.release_write()

    def find(self, collection, query=None):
        """Fast indexed queries with read lock, supporting multiple conditions."""
        self.rw_lock.acquire_read()
        try:
            if not query:
                return list(self.data.get(collection, {}).values())

            indexed_results = None
            for field, condition in query.items():
                if field in self.indexes:
                    possible_keys = set()

                    if isinstance(condition, dict):
                        if "$eq" in condition:
                            possible_keys = self.indexes[field].get(condition["$eq"], set())
                        if "$in" in condition:
                            for val in condition["$in"]:
                                possible_keys.update(self.indexes[field].get(val, set()))
                        if "$ne" in condition:
                            all_keys = set(self.data.get(collection, {}))
                            exclude_keys = self.indexes[field].get(condition["$ne"], set())
                            possible_keys = all_keys - exclude_keys
                        if "$gt" in condition or "$gte" in condition:
                            for key, values in self.indexes[field].items():
                                if ("$gt" in condition and key > condition["$gt"]) or ("$gte" in condition and key >= condition["$gte"]):
                                    possible_keys.update(values)
                        if "$lt" in condition or "$lte" in condition:
                            for key, values in self.indexes[field].items():
                                if ("$lt" in condition and key < condition["$lt"]) or ("$lte" in condition and key <= condition["$lte"]):
                                    possible_keys.update(values)
                    else:
                        possible_keys = self.indexes[field].get(condition, set())

                    if indexed_results is None:
                        indexed_results = possible_keys
                    else:
                        indexed_results &= possible_keys

            if indexed_results is not None:
                return [self.data[collection][key] for key in indexed_results if key in self.data[collection]]

            return []
        finally:
            self.rw_lock.release_read()

    def _backup_data(self, backup_file="backup.db"):
        """Creates a full backup of the database."""
        self.rw_lock.acquire_read()
        try:
            shutil.copy2(self.storage_file, backup_file)
            shutil.copy2(self.index_file, backup_file + ".idx")
            self.logger.info(f"Backup created successfully: {backup_file}")
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
        finally:
            self.rw_lock.release_read()
    
    def _restore_data(self, backup_file="backup.db"):
        """Restores the database from a backup file."""
        self.rw_lock.acquire_write()
        try:
            if os.path.exists(backup_file) and os.path.exists(backup_file + ".idx"):
                shutil.copy2(backup_file, self.storage_file)
                shutil.copy2(backup_file + ".idx", self.index_file)
                self._load_data()
                self._load_indexes()
                self.logger.info("Database restored successfully from backup.")
            else:
                self.logger.error("Backup file(s) not found. Restore failed.")
        except Exception as e:
            self.logger.error(f"Error restoring backup: {e}")
        finally:
            self.rw_lock.release_write()
    
    def schedule_backup(self, interval=3600, backup_file="backup.db"):
        """Schedules periodic backups."""
        def backup_task():
            while True:
                time.sleep(interval)
                self._backup_data(backup_file)
        
        backup_thread = threading.Thread(target=backup_task, daemon=True)
        backup_thread.start()
        self.logger.info("Automatic backup scheduled.")