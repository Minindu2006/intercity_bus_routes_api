from typing import Optional

from starlette import status
from starlette.exceptions import HTTPException

from models import BusRouteResponse, BusRouteCreate
from repository import BusRouteRepository


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
