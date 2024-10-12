import motor.motor_asyncio
from pymongo import MongoClient
from bson import ObjectId

# MongoDB connection
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017") #You can change this with Atlas cluster if your are using it.
db = client["mydb"]  # Replace with your actual database name

# Define collections
item_collection = db["items"]
clockin_collection = db["clockins"]

# Helper functions for object ID conversion
def convert_id(item):
    item["id"] = str(item.pop("_id"))
    return item

async def get_item(item_id: str):
    item = await item_collection.find_one({"_id": ObjectId(item_id)})
    return convert_id(item) if item else None

async def get_clockin(clockin_id: str):
    clockin = await clockin_collection.find_one({"_id": ObjectId(clockin_id)})
    return convert_id(clockin) if clockin else None
