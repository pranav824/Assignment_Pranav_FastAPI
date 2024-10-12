from fastapi import FastAPI
from app.routes.item_routes import router as item_router
from app.routes.clockin_routes import router as clockin_router

app = FastAPI()

# Register routes
app.include_router(item_router, prefix="/items", tags=["Items"])
app.include_router(clockin_router, prefix="/clock-in", tags=["Clock-In Records"])

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI MongoDB CRUD Application!"}
