from erioon.storage import ErioonDB
import shelve

db = ErioonDB()

with db.transaction(): 
    db.insert("users", {"name": "Charlie", "age": 35})
    db.insert("users", {"name": "Diana", "age": 28})
    db.insert("products", {"name": "Laptop", "price": 1200})
    db.insert("products", {"name": "Phone", "price": 800})

with shelve.open("store.db") as db_file:
    print("Keys in DB:", db_file.keys())  
    print("Users collection:", db_file.get("users", {}))
    print("Products collection:", db_file.get("products", {}))  