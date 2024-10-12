from bson import ObjectId
from datetime import date

def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "item_name": item["item_name"],
        "quantity": item["quantity"],
        "expiry_date": str(item["expiry_date"]),
        "insert_date": str(item["insert_date"]),
    }
