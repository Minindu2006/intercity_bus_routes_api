from typing import Optional, List
from psycopg2.extras import RealDictCursor

from database import get_db_connection
from models import BusRouteResponse, BusRouteCreate, BusRouteUpdate, ScheduleCreate, ScheduleResponse, \
    BusRoutesWithSchedules


class BusRouteRepository:
    def get_by_id(self, route_id: int) -> Optional[BusRouteResponse]:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM bus_routes where id=%s;", (route_id,))
        route = cursor.fetchone()

        cursor.close()
        connection.close()

        return BusRouteResponse(**route) if route else None

    def get_by_id_with_schedules(self, route_id) -> Optional[BusRoutesWithSchedules]:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = """
            select routes.route_number
            ,routes.id as route_id
            ,routes.start_location
            ,routes.end_location
            ,routes.bus_type
            ,routes.ticket_price
            ,sch.id as schedule_id
            ,sch.departure_time
            ,sch.arrival_time
            ,sch.available_seats 
            ,sch.status 
            from bus_routes routes
            left join schedules sch on sch.route_id = routes.id
            where routes.id = %s
            order by sch.departure_time asc nulls last;
            ;
        """
        try:
            cursor.execute(query, (route_id, ))
            schedules = cursor.fetchall()

            if not schedules:
                return None

            route = BusRoutesWithSchedules(
                route_number=schedules[0]["route_number"],
                start_location=schedules[0]["start_location"],
                end_location=schedules[0]["end_location"],
                bus_type=schedules[0]["bus_type"],
                ticket_price=schedules[0]["ticket_price"],
                id = route_id,
                schedules=[]
            )

            for schedule in schedules:
                if schedule["schedule_id"] is not None:
                    route.schedules.append(ScheduleResponse(
                        id=schedule["schedule_id"],
                        departure_time=schedule["departure_time"],
                        arrival_time=schedule["arrival_time"],
                        available_seats=schedule["available_seats"],
                        status=schedule["status"],
                        route_id=route_id
                    ))
            return route
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()


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

    def update_record(self, bus_route: BusRouteUpdate, route_id: int) -> Optional[BusRouteResponse]:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = """
            UPDATE bus_routes
            SET route_number = %s,
            start_location = %s,
            end_location = %s,
            bus_type = %s,
            ticket_price = %s WHERE id = %s
            RETURNING *;
        """
        try:
            cursor.execute(
                query,
                (bus_route.route_number, bus_route.start_location, bus_route.end_location, bus_route.bus_type, bus_route.ticket_price, route_id)
            )
            updated_route = cursor.fetchone()
            connection.commit()
            return BusRouteResponse(**updated_route)
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()



class ScheduleRepository:
    def create_schedule(self, route_id: int, schedule: ScheduleCreate) -> Optional[ScheduleCreate]:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = """
            INSERT INTO schedules
            (route_id, departure_time, arrival_time, available_seats, status)
            VALUES (%s, %s::TIME, %s::TIME, %s, %s)
            RETURNING *
        """
        try:
            cursor.execute(query, (route_id, schedule.departure_time, schedule.arrival_time, schedule.available_seats, schedule.status))
            new_schedule = cursor.fetchone()
            connection.commit()
            return ScheduleResponse(**new_schedule)

        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()
