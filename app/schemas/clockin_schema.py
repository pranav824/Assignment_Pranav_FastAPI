from bson import ObjectId
from datetime import datetime

def clockin_helper(clockin) -> dict:
    return {
        "id": str(clockin["_id"]),  # Access the ID from the MongoDB document
        "email": clockin["email"],
        "location": clockin["location"],
        "insert_date": clockin["insert_date"],
    }

