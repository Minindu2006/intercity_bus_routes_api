from typing import Optional, List

from fastapi import APIRouter
from starlette import status

from models import BusRouteResponse, BusRouteCreate, BusRouteUpdate, ScheduleResponse, ScheduleCreate
from repository import BusRouteRepository, ScheduleRepository
from service import BusRouteService, ScheduleService

router = APIRouter(
    prefix="/routes"
)
repo = BusRouteRepository()
repoS = ScheduleRepository()
busService = BusRouteService(repo)
scheduleService = ScheduleService(repoS)

@router.get(
    "/{route_id}", # Path variables
    response_model=Optional[BusRouteResponse],
    status_code=status.HTTP_200_OK
)
def get_route_by_id(route_id):
    route = busService.get_by_id(route_id)
    return route

@router.get(
    "",
    response_model=List[BusRouteResponse],
    status_code=status.HTTP_200_OK
)
def get_all_routes(offset: int = 0, limit: int = 10): # Query Parameters
    routes = busService.get_all_routes(offset, limit)
    return routes

@router.post(
    "/",
    response_model=BusRouteResponse,
    status_code=status.HTTP_201_CREATED
)
def create_bus_route(router_request: BusRouteCreate):
    return busService.create_bus_route(router_request)

@router.delete(
    "/{route_id}",
    status_code=status.HTTP_200_OK
)
def delete_record(route_id: int):
    return "successfully deleted" if busService.delete_record(route_id) else None

@router.put(
    "/{route_id}",
    response_model=Optional[BusRouteResponse],
    status_code=status.HTTP_200_OK
)
def update_record(route_id: int, router_request: BusRouteUpdate):
    return busService.update_record(router_request, route_id)

@router.post(
    '/schedules/{route_id}',
    response_model=ScheduleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_schedule(route_id: int, schedule: ScheduleCreate):
    return scheduleService.create_schedule(route_id, schedule)