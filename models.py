from pydantic import BaseModel, Field
from datetime import time

class BusRouteCreate(BaseModel):
    route_number: str = Field(...,max_length=50)
    start_location: str = Field(..., max_length=100)
    end_location: str = Field(..., max_length=100)
    bus_type: str = Field(..., max_length=50)
    ticket_price: float = Field(..., ge=0)

class BusRouteUpdate(BusRouteCreate):
    pass

class BusRouteResponse(BusRouteCreate):
    id: int

class ScheduleCreate(BaseModel):
    departure_time: time = Field(...)
    arrival_time: time = Field(...)
    available_seats: int = Field(...,ge=0, le=100)
    status: str = Field(..., max_length=20)

class ScheduleResponse(ScheduleCreate):
    id: int
    route_id: int