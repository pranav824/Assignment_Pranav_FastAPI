from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timedelta

class Item(BaseModel):
    id: Optional[str] = None 
    name: str
    email: str
    item_name: str
    quantity: int
    expiry_date: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(days=30))
    insert_date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Add created_at
    description: str

    class Config:
        orm_mode = True