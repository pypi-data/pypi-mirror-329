import os
from ErioonDB.database import Database  # Import Database to interact with data
from ErioonDB.auth import Auth

class ErioonClient:
    def __init__(self, auth_string):
        """
        Initialize ErioonClient with authentication using Auth class.
        Expected format: "API_KEY/email:password"
        """
        self.db_directory = "./db"
        self.auth = Auth()

        # Authenticate using Auth class
        self.authenticated, self.user_email, self.api_key = self.auth.authenticate(auth_string)

        if not self.authenticated:
            raise ValueError("Authentication failed. Invalid API Key or credentials.")

        # Ensure DB directory exists
        if not os.path.exists(self.db_directory):
            os.makedirs(self.db_directory)

    def __call__(self, db_name):
        """Retrieve an existing database or create a new one if it doesn't exist."""
        db_path = os.path.join(self.db_directory, db_name)
        
        # Check if the user database exists or needs to be created
        if not os.path.exists(db_path):
            print(f"Database '{db_name}' does not exist. Creating it now...")
            # If the database doesn't exist, create it and initialize default databases
            return self.create_database(db_name)
        else:
            # If the user database exists, return the Database instance
            return Database(db_name)

    def create_database(self, db_name):
        """Create a new user database and initialize system and rules databases."""
        db_path = os.path.join(self.db_directory, db_name)
        if not os.path.exists(db_path):
            os.makedirs(db_path)
            print(f"Database '{db_name}' created.")

        # Initialize the user Database instance
        user_db = Database(db_name)

        # Initialize system and rules databases if they don't exist
        self._initialize_system_and_rules_dbs()

        return user_db

    def _initialize_system_and_rules_dbs(self):
        """Initialize system and rules databases if they don't exist."""
        for default_db_name in ['system', 'rules']:
            if not os.path.exists(os.path.join(self.db_directory, default_db_name)):
                print(f"Initializing system database '{default_db_name}'.")
                # Create system and rules databases
                Database(default_db_name)

            # Ensure the default collections exist in these system databases
            self._initialize_default_collections(default_db_name)

    def _initialize_default_collections(self, db_name):
        """Initialize default collections in system and rules databases."""
        system_db = Database(db_name)

        # Create default collections like configuration and rules for the 'system' and 'rules' databases
        if db_name == 'system':
            # Add system-specific collections (e.g., system settings, application configurations)
            system_db['configurations']
            system_db['users']  # For example, store application users in system database
        elif db_name == 'rules':
            # Add rule-specific collections (e.g., validation rules, access rules)
            system_db['access_rules']
            system_db['validation_rules']
