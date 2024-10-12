from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ClockIn(BaseModel):
    id: Optional[str] = None 
    email: EmailStr
    location: str
    insert_datetime: Optional[datetime] = None

    class Config:
        orm_mode = True
   
