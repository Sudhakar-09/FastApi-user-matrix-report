from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    role: str


class UserUpdate(BaseModel):
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str]
    address: Optional[str]
    role: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        orm_mode = True


class StatusResponse(BaseModel):
    status: str
    message: str

# Define the response model for the full report
class UserReportResponse(BaseModel):
    status: str
    message: str
    data: List[dict]

class UserReportItem(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    site_roles: List[str]
    organizations: List[str]
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        orm_mode = True