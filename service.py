from typing import Optional

from starlette import status
from starlette.exceptions import HTTPException

from models import BusRouteResponse, BusRouteCreate, BusRouteUpdate, ScheduleCreate
from repository import BusRouteRepository, ScheduleRepository


class BusRouteService:
    def __init__(self, repo: BusRouteRepository):
        self.repo = repo

    def get_by_id(self, route_id: int) -> Optional[BusRouteResponse]:
        route = self.repo.get_by_id(route_id)

        if not route:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus Route not found")

        return route

    def get_all_routes(self, offset: int, limit: int):
        routes = self.repo.get_all(offset, limit)

        if not routes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bus routes available")
        return routes

    def create_bus_route(self, bus_route: BusRouteCreate) -> BusRouteResponse:
        try:
            return self.repo.create_bus_route(bus_route)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create a record : {str(e)}")

    def delete_record(self, route_id: int) -> bool:
        try:
            deleted = self.repo.delete_record(route_id)

            if not deleted:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No bus routes available with id {route_id}")
            else:
                return True

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete record with id {route_id} : {str(e)}")

    def update_record(self, bus_route: BusRouteUpdate, route_id: int):
        try:
            updated = self.repo.update_record(bus_route, route_id)

            if not updated:
                raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                                    detail=f"Error hrn modifying bus route with id {route_id}")
            return updated

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Failed to update record with id {route_id} : {str(e)}")


class ScheduleService:
    def __init__(self, repo: ScheduleRepository):
        self.repo = repo

    def create_schedule(self, route_id: int, schedule: ScheduleCreate):
        try:
            return self.repo.create_schedule(route_id, schedule)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create a record : {str(e)}")