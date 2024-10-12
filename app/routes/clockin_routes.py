from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from app.database import clockin_collection
from app.schemas.clockin_schema import clockin_helper
from app.models.clockin_model import ClockIn
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.mydb  # Replace 'mydb' with your actual database name


# Create a clock-in record
@router.post("/clock-in", status_code=201)
async def create_clock_in(clock_in: ClockIn):
    clock_in_data = clock_in.dict()  # Convert Pydantic model to dictionary
    clock_in_data["insert_date"] = datetime.utcnow()  # Set insert date to current time

    try:
        result = await db.clockins.insert_one(clock_in_data)
        return {"id": str(result.inserted_id), "message": "Clock-in entry created successfully."}
    except Exception as e:
        print(f"Error creating clock-in: {e}")  # Debugging output
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Get clock-in by ID
@router.get("/{clockin_id}")
async def get_clockin(clockin_id: str):
    print(f"Received request for clock-in ID: {clockin_id}")

    if not ObjectId.is_valid(clockin_id):
        print("Invalid ID format")
        raise HTTPException(status_code=400, detail="Invalid ID format")

    clockin_record = await clockin_collection.find_one({"_id": ObjectId(clockin_id)})
    if clockin_record is None:
        print("No clock-in record found")
        raise HTTPException(status_code=404, detail="Clock-in record not found")

    print("Clock-in record found:", clockin_record)
    return clockin_record

# Filter clock-ins
@router.get("/filter")
async def filter_clockins(email: str = None, location: str = None, insert_datetime: datetime = None):
    query = {}
    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if insert_datetime:
        query["insert_datetime"] = {"$gt": insert_datetime}

    records = clockin_collection.find(query)
    return [clockin_helper(record) for record in records]

# Update a clock-in record
@router.put("/{id}")
async def update_clockin(id: str, clockin: ClockIn):
    updated_clockin = clockin.dict(exclude_unset=True)
    updated_clockin.pop("insert_datetime", None)
    result = clockin_collection.update_one({"_id": ObjectId(id)}, {"$set": updated_clockin})
    if result.matched_count:
        return {"message": "Clock-in record updated successfully!"}
    raise HTTPException(status_code=404, detail="Clock-in record not found")

# Delete a clock-in record
@router.delete("/{id}")
async def delete_clockin(id: str):
    result = clockin_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return {"message": "Clock-in record deleted successfully!"}
    raise HTTPException(status_code=404, detail="Clock-in record not found")


