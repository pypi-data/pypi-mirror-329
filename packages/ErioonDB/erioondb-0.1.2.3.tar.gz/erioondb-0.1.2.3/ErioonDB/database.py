import os
import avro.schema
import avro.io
import logging
from threading import Lock
from avro.datafile import DataFileWriter, DataFileReader
from avro.io import DatumWriter, DatumReader
from .collection import Collection 

class Database:
    def __init__(self, db_name, db_directory="./db"):
        self.db_name = db_name
        self.db_directory = db_directory
        self.storage_dir = os.path.join(self.db_directory, db_name)
        self.data = {}
        self.logger = logging.getLogger(__name__)
        self.lock = Lock()
        self.schemas = {}

        os.makedirs(self.storage_dir, exist_ok=True)

    def set_schema(self, collection_name, schema_json):
        """Sets the schema for a collection."""
        try:
            if isinstance(schema_json, str):
                schema = avro.schema.Parse(schema_json)  # Parse the schema if it's a JSON string
            elif isinstance(schema_json, dict):
                schema = avro.schema.SchemaFromJSONData(schema_json)  # Parse if it's a dictionary
            else:
                raise ValueError("Schema must be a string or dictionary.")

            self.schemas[collection_name] = schema

            # Save schema to a file for later use
            schema_path = self.get_schema_path(collection_name)
            with open(schema_path, "w") as f:
                f.write(schema_json if isinstance(schema_json, str) else str(schema_json))

            self.logger.info(f"Schema for collection '{collection_name}' set successfully.")
        except Exception as e:
            self.logger.error(f"Error setting schema for collection '{collection_name}': {e}")

    def get_schema_path(self, collection_name):
        """Returns the path to the schema file for the collection."""
        return os.path.join(self.storage_dir, f"{collection_name}_schema.json")
    
    def get_collection_path(self, collection_name):
        return os.path.join(self.storage_dir, f"{collection_name}.avro")

    def _load_collection(self, collection_name):
        """Load collection data from its corresponding Avro file."""
        collection_file = os.path.join(self.storage_dir, f"{collection_name}.avro")
        if os.path.exists(collection_file):
            try:
                with open(collection_file, "rb") as f:
                    reader = DataFileReader(f, DatumReader())
                    collection_data = [record for record in reader]
                self.logger.info(f"Collection '{collection_name}' loaded successfully.")
                return collection_data
            except Exception as e:
                self.logger.error(f"Error loading collection '{collection_name}' from Avro: {e}")
                return []
        else:
            self.logger.info(f"Collection '{collection_name}' not found, creating a new one.")
            return []

    def _save_collection(self, collection_name, data):
        """Save collection data to its corresponding Avro file."""
        collection_file = os.path.join(self.storage_dir, f"{collection_name}.avro")
        schema = self.schemas.get(collection_name)

        if schema is None:
            self.logger.error(f"No schema found for collection '{collection_name}', unable to save data.")
            return

        try:
            with open(collection_file, "wb") as f:
                writer = DataFileWriter(f, DatumWriter(), schema)
                for record in data:
                    writer.append(record)
                writer.close()
            self.logger.info(f"Collection '{collection_name}' saved successfully in Avro format.")
        except Exception as e:
            self.logger.error(f"Error saving collection '{collection_name}' to Avro: {e}")

    def __getitem__(self, collection_name):
        """Retrieve or create a collection within this database."""
        with self.lock:  # Ensure thread safety while accessing the data
            if collection_name not in self.data:
                # Load the collection data from the corresponding Avro file
                self.data[collection_name] = self._load_collection(collection_name)
            return Collection(self, collection_name)  # Assuming you have a Collection class

    def flush(self):
        """Clear the entire database (similar to Redis FLUSHDB)."""
        with self.lock:  # Ensure thread safety while modifying the data
            for collection_name in self.data:
                self._save_collection(collection_name, [])  # Reset collections to empty files
            self.logger.warning(f"Database '{self.db_name}' has been flushed.")

    def backup(self):
        """Create a backup of the database (copy the collection Avro files to a backup location)."""
        backup_dir = os.path.join(self.db_directory, "backups")
        os.makedirs(backup_dir, exist_ok=True)

        try:
            for collection_name in self.data:
                collection_file = os.path.join(self.storage_dir, f"{collection_name}.avro")
                backup_file = os.path.join(backup_dir, f"{self.db_name}_{collection_name}_backup.avro")
                # Copy the collection file
                with open(collection_file, "rb") as original_file:
                    data = original_file.read()
                with open(backup_file, "wb") as backup_file:
                    backup_file.write(data)
                self.logger.info(f"Backup for collection '{collection_name}' created at '{backup_file}'.")
        except Exception as e:
            self.logger.error(f"Error creating backup for database '{self.db_name}': {e}")

    def restore_backup(self, collection_name, backup_name):
        """Restore a collection from a backup."""
        backup_dir = os.path.join(self.db_directory, "backups")
        backup_file = os.path.join(backup_dir, backup_name)

        if os.path.exists(backup_file):
            try:
                with open(backup_file, "rb") as f:
                    reader = DataFileReader(f, DatumReader())
                    backup_data = [record for record in reader]
                self.data[collection_name] = backup_data
                self._save_collection(collection_name, backup_data)  # Persist restored data
                self.logger.info(f"Collection '{collection_name}' restored from backup '{backup_name}'.")
            except Exception as e:
                self.logger.error(f"Error restoring collection '{collection_name}' from backup: {e}")
        else:
            self.logger.error(f"Backup file '{backup_name}' not found in the backup directory.")

    def validate(self):
        """Perform basic validation of the database's content."""
        valid = True
        for collection_name, collection_data in self.data.items():
            # Example validation: ensure collections contain dicts or lists as data
            if not isinstance(collection_data, list):
                self.logger.warning(f"Collection '{collection_name}' contains invalid data format.")
                valid = False
        return valid

    def insert(self, collection_name, record):
        """Insert a record into the collection."""
        collection_data = self._load_collection(collection_name)
        collection_data.append(record)
        self._save_collection(collection_name, collection_data)
        self.logger.info(f"Record inserted into collection '{collection_name}'.")

    def retrieve(self, collection_name, record_id):
        """Retrieve a record by its ID."""
        collection_data = self._load_collection(collection_name)
        for record in collection_data:
            if record.get("id") == record_id:
                self.logger.info(f"Record retrieved: {record}")
                return record
        self.logger.warning(f"Record with ID '{record_id}' not found in collection '{collection_name}'.")
        return None

    def delete(self, collection_name, record_id):
        """Delete a record by its ID."""
        collection_data = self._load_collection(collection_name)
        collection_data = [record for record in collection_data if record.get("id") != record_id]
        self._save_collection(collection_name, collection_data)
        self.logger.info(f"Record with ID '{record_id}' deleted from collection '{collection_name}'.")
