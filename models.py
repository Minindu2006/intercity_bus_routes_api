from pydantic import BaseModel, Field


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
    