from typing import Optional, List
from psycopg2.extras import RealDictCursor

from database import get_db_connection
from models import BusRouteResponse, BusRouteCreate


class BusRouteRepository:
    def get_by_id(self, route_id: int) -> Optional[BusRouteResponse]:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM bus_routes where id=%s;", (route_id,))
        route = cursor.fetchone()

        cursor.close()
        connection.close()

        return BusRouteResponse(**route) if route else None

    def get_all(self, offset: int = 0, limit: int = 20) -> List[BusRouteResponse]:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM bus_routes order by id ASC OFFSET %s LIMIT %s", (offset, limit))
        routes = cursor.fetchall()

        cursor.close()
        connection.close()
        return [BusRouteResponse(**route) for route in routes]

    def create_bus_route(self, bus_route: BusRouteCreate) -> BusRouteResponse:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = """
            INSERT INTO bus_routes
            (route_number, start_location, end_location, bus_type, ticket_price)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
        """

        try:
            cursor.execute(query, (bus_route.route_number, bus_route.start_location, bus_route.end_location, bus_route.bus_type, bus_route.ticket_price))
            new_route = cursor.fetchone()
            connection.commit()
            return BusRouteResponse(**new_route)

        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()

    def delete_record(self, route_id: int) -> bool:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = "DELETE FROM bus_routes WHERE id = %s"
        try:
            cursor.execute(
                query,
                (route_id,)
            )
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()

