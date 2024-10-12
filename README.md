# FastAPI CRUD Application

This FastAPI application provides CRUD operations for two entities: Items and User Clock-In Records. It uses MongoDB as the database and includes APIs for managing both entities.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Motor (Async MongoDB driver)
- Pydantic

## Setup

### 1. MongoDB Setup

- Set up a MongoDB database using [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) or run a local MongoDB instance.
- Create two collections: `items` and `clockins`.

### 2. Install Dependencies

pip install fastapi uvicorn motor pydantic python-dotenv

Run the server - uvicorn app.main:app --reload


