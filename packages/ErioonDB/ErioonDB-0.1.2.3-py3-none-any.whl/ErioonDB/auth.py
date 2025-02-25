from dotenv import load_dotenv
import os
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
load_dotenv()

class Auth:
    def __init__(self):
        """Connect to MongoDB Atlas for authentication."""
        self.uri =  self.uri = os.getenv("MONGO_URI")
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client["erioonDB"]

    def authenticate(self, auth_string):
        """
        Authenticate using API Key, Email & Password.
        Expected format: "API_KEY/email:password"
        Returns: (authenticated: bool, user_email: str, api_key: str)
        """
        try:
            # Split auth_string into API Key and Credentials (email:password)
            api_key, credentials = auth_string.split("/")
            email, password = credentials.split(":")
        except ValueError:
            raise ValueError("Invalid authentication format. Expected 'API_KEY/email:password'.")

        # Check if the API Key is valid
        if not self.authenticate_api_key(api_key):
            print("Invalid API Key.")
            return False, None, None

        # Check if the Email exists
        if not self.authenticate_email(email):
            print("Invalid Email.")
            return False, None, None

        # Check if the Password is correct
        if not self.authenticate_password(email, password):
            print("Incorrect Password.")
            return False, None, None

        # If all checks pass, return authentication success
        print(f"Authentication successful for email: {email}")
        return True, email, api_key

    def authenticate_api_key(self, api_key):
        """Authenticate API Key by checking inside apis.{id_api}.key in MongoDB."""
        users_collection = self.db["users"]

        # Search in all users to find a matching API key
        for user in users_collection.find():
            for id_api, api_data in user.get("apis", {}).items():
                if api_data.get("key") == api_key:
                    return True
        return False

    def authenticate_email(self, email):
        """Authenticate email by checking if it exists in personal_info.email."""
        users_collection = self.db["users"]

        # Find the user by email
        user = users_collection.find_one({"personal_info.email": email})
        if user:
            return True
        print(f"Email not found: {email}")
        return False

    def authenticate_password(self, email, password):
        """Authenticate user by checking personal_info.email and personal_info.password in MongoDB."""
        users_collection = self.db["users"]

        # Find the user by email
        user = users_collection.find_one({"personal_info.email": email})

        if user:
            # Compare hashed password in the database with the provided password
            stored_hashed_password = user["personal_info"]["password"]
            if check_password_hash(stored_hashed_password, password):
                return True
            else:
                print("Incorrect password.")
                return False
        print(f"No user found for email: {email}")
        return False
