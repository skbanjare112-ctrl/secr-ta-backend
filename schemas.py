from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    hrms_id: str
    password: str = Field(min_length=6)
    full_name: str = ""
    department: str = ""
    division: str = ""
    headquarter: str = ""
    pf_no: str = ""
    designation: str = ""
    pay: float = 0
    scale_of_pay: str = ""
    bill_unit_no: str = ""

class UserOut(BaseModel):
    id: int
    hrms_id: str
    full_name: str
    department: str
    division: str
    headquarter: str
    pf_no: str
    designation: str
    pay: float
    scale_of_pay: str
    bill_unit_no: str
    is_admin: bool
    is_active: bool
    class Config:
        from_attributes = True

class TravelCreate(BaseModel):
    journey_date: str
    transport_mode: str = ""
    train_no: str = ""
    departure_time: str = ""
    arrival_time: str = ""
    from_station: str = ""
    to_station: str = ""
    kms: float = 0
    days: float = 0
    nights: float = 0
    object_for_journey: str = ""
    rate: float = 625
    percentage: float = 100

class TravelOut(TravelCreate):
    id: int
    user_id: int
    amount: float
    created_at: datetime
    class Config:
        from_attributes = True
