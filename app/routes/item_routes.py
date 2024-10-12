from fastapi import APIRouter, HTTPException, status
from pymongo.collection import Collection
from app.models.item_model import Item
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from datetime import datetime
from app.database import db

router = APIRouter()

# Reference to MongoDB collection
items_collection: Collection = None  # This will be set in the app initialization

# POST /items: Create a new item
@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    item_data = item.dict(exclude_unset=True)  # Prepare item data, excluding unset fields

    try:
        # Insert the item into the MongoDB collection
        result = await db.items.insert_one(item_data)

        # Fetch the inserted item to return it with the generated ObjectId
        if result.inserted_id:
            inserted_item = await db.items.find_one({"_id": result.inserted_id})

            # Convert ObjectId to string and return the item
            inserted_item["id"] = str(inserted_item["_id"])  # Convert ObjectId to string
            return inserted_item
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# GET /items/{id}: Retrieve an item by ID
@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: str):
    # Validate ObjectId
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    
    try:
        # Query the database for the item
        item = await db.items.find_one({"_id": ObjectId(item_id)})
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        item["id"] = str(item["_id"])  # Convert the ObjectId to string before returning
        return item
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error retrieving item")
    
# GET /items/filter: Filter items based on email, expiry date, insert date, and quantity
@router.get("/filter/")
async def filter_items(email: str = None, expiry_date: str = None, insert_date: str = None, quantity: int = None):
    query = {}
    
    if email:
        query['email'] = email
    if expiry_date:
        query['expiry_date'] = {"$gte": datetime.strptime(expiry_date, "%Y-%m-%d")}
    if insert_date:
        query['insert_date'] = {"$gte": datetime.strptime(insert_date, "%Y-%m-%d")}
    if quantity:
        query['quantity'] = {"$gte": quantity}
    
    try:
        items = list(items_collection.find(query))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# MongoDB aggregation: Count of items for each email
@router.get("/aggregate/count-by-email/")
async def count_items_by_email():
    try:
        pipeline = [
            {"$group": {"_id": "$email", "count": {"$sum": 1}}}
        ]
        result = await db.items.aggregate(pipeline).to_list(length=None)

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found")

        return result
    except Exception as e:
        print(f"Error during aggregation: {e}")  # Debugging output
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
# DELETE /items/{id}: Delete an item by ID
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str):
    item_id = item_id.strip()
    print(f"Received item_id for deletion: '{item_id}'")  # Debugging output

    # Validate ObjectId
    if not ObjectId.is_valid(item_id):
        print("Invalid ObjectId format")  # Debugging output
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")

    try:
        result = await db.items.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 0:
            print("No item found with the provided ID")  # Debugging output
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    except Exception as e:
        print(f"Error deleting item with ID {item_id}: {e}")  # Debugging output
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

# PUT /items/{id}: Update an item by ID (excluding insert_date)
@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    item_id = item_id.strip()
    print(f"Received item_id for update: '{item_id}'")  # Debugging output

    # Validate ObjectId
    if not ObjectId.is_valid(item_id):
        print("Invalid ObjectId format")  # Debugging output
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")

    item_data = item.dict()

    # Update the item in the database
    try:
        result = await db.items.update_one({"_id": ObjectId(item_id)}, {"$set": item_data})
        if result.modified_count == 0:
            print("No item found with the provided ID or no changes made")  # Debugging output
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found or no changes made")

        # Fetch the updated item to return it
        updated_item = await db.items.find_one({"_id": ObjectId(item_id)})
        return updated_item
    except Exception as e:
        print(f"Error updating item with ID {item_id}: {e}")  # Debugging output
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")