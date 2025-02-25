import os
import json
import fastavro
from fastavro import writer, reader, parse_schema
import uuid


class Collection:
    def __init__(self, database, collection_name):
        self.database = database
        self.collection_name = collection_name
        self.schema = None  # Initialize schema as None
        self.schema_file = self.database.get_schema_path(self.collection_name)
        
        # Load schema if it exists
        self._load_schema()
        
    def _load_schema(self):
        """Load the schema for this collection from an Avro schema file."""
        if os.path.exists(self.schema_file):
            with open(self.schema_file, "r", encoding="utf-8") as f:
                self.schema = json.load(f)
            print(f"Schema loaded for collection '{self.collection_name}'.")
        else:
            print(f"No schema found for collection '{self.collection_name}', unable to save data.")

    def set_schema(self, schema):
        """Set the schema for this collection."""
        self.schema = schema
        print(f"Setting schema for {self.collection_name}: {self.schema}")  # Debugging output

        # Ensure the schema contains the necessary fields like 'type' and 'fields'
        if 'type' not in self.schema or 'fields' not in self.schema:
            print("Error: Schema must contain the 'type' and 'fields' fields.")
            return

        # Save schema as JSON
        with open(self.schema_file, "w", encoding="utf-8") as f:
            json.dump(self.schema, f, indent=4)

        print(f"Schema set for collection '{self.collection_name}'.")


    def _load_collection(self):
        """Load data from the Avro file."""
        collection_file = self.database.get_collection_path(self.collection_name)
        if os.path.exists(collection_file):
            with open(collection_file, 'rb') as f:
                return list(reader(f))
        return []

    def _save_collection(self, data):
        """Save the data to the Avro file."""
        collection_file = self.database.get_collection_path(self.collection_name)
        with open(collection_file, 'wb') as f:
            writer(f, self.schema, data)

    def insert_one(self, object):
        """Insert a new item into the collection."""
        schema = self.schema

        if schema is None:
            print(f"Error: No schema found for collection '{self.collection_name}'.")
            return

        # Automatically assign a UUID to the 'id' field if not already present
        if 'id' not in object:
            object['id'] = str(uuid.uuid4())  # Generate a unique UUID

        # Validate data against the schema
        try:
            if not fastavro.validate(object, schema):
                print(f"Error: Value does not match the schema for collection '{self.collection_name}'.")
                return
        except Exception as e:
            print(f"Error validating schema for collection '{self.collection_name}': {e}")
            return

        # Proceed with inserting data after validation
        collection_data = self._load_collection()
        collection_data.append(object)

        # Save the updated collection to the file
        self._save_collection(collection_data)
        print(f"Item inserted into collection '{self.collection_name}' with key '{object['id']}'.")


    def insert_many(self, objects):
        """Insert multiple items into the collection."""
        schema = self.schema

        if schema is None:
            print(f"Error: No schema found for collection '{self.collection_name}'.")
            return

        # Validate and assign UUIDs to the objects
        valid_objects = []
        for obj in objects:
            if 'id' not in obj:
                obj['id'] = str(uuid.uuid4())  # Generate a unique UUID
            # Validate each object against the schema
            try:
                if fastavro.validate(obj, schema):
                    valid_objects.append(obj)
                else:
                    print(f"Error: Object does not match the schema for collection '{self.collection_name}'. Skipping object.")
            except Exception as e:
                print(f"Error validating object: {e}. Skipping object.")
        
        if valid_objects:
            collection_data = self._load_collection()
            collection_data.extend(valid_objects)
            self._save_collection(collection_data)
            print(f"{len(valid_objects)} items inserted into collection '{self.collection_name}'.")
        else:
            print(f"No valid items were inserted into collection '{self.collection_name}'.")

    def update_one(self, condition, new_value):
        """Update an existing item in the collection based on a condition."""
        if self.schema is None:
            print(f"Warning: No schema found for collection '{self.collection_name}'.")
            return

        # Load existing records
        records = self._load_collection()

        updated_count = 0
        for record in records:
            # Check if the record matches the condition (which can be any key-value pair)
            if all(record.get(key) == value for key, value in condition.items()):
                record.update(new_value)  # Update the record with new_value
                updated_count += 1

        if updated_count > 0:
            # Save the updated records back to the Avro file
            self._save_collection(records)
            print(f"Updated {updated_count} items in collection '{self.collection_name}'.")
        else:
            print(f"No records matching the condition '{condition}' found to update.")

        
    def update_many(self, condition, new_value):
        """Update multiple items in the collection based on a condition."""
        if self.schema is None:
            print(f"Warning: No schema found for collection '{self.collection_name}'.")
            return
    
        # Load existing records
        records = self._load_collection()
    
        updated_count = 0
        for record in records:
            # Check if the record matches the condition (which can be any key-value pair)
            if all(record.get(key) == value for key, value in condition.items()):
                record.update(new_value)  # Update the record with new_value
                updated_count += 1
    
        if updated_count > 0:
            # Save the updated records back to the Avro file
            self._save_collection(records)
            print(f"Updated {updated_count} items in collection '{self.collection_name}'.")
        else:
            print(f"No records matching the condition '{condition}' found to update.")
    

    def delete_one(self, key):
        """Delete an item from the collection (in the Avro file)."""
        if self.schema is None:
            print(f"Warning: No schema found for collection '{self.collection_name}'.")
            return

        # Load existing records
        records = self._load_collection()

        # Find and remove the record by key
        records = [record for record in records if record.get('id') != key]

        # Save the updated records back to the Avro file
        self._save_collection(records)
        print(f"Deleted item with key '{key}' from collection '{self.collection_name}'.")

    def get_one(self, key):
        """Get an item from the collection (from the Avro file)."""
        records = self._load_collection()
        for record in records:
            if record.get('id') == key:
                return record
        return None

    def get_all(self):
        """Get all items from the collection (from the Avro file)."""
        records = self._load_collection()
        return records
