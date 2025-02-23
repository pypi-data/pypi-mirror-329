"""This module contains the code to get weather data from an MYSQL Table."""
from __future__ import annotations

import logging
import mysql.connector

from .data import ForecastDaily, ForecastHourly, MinuteData, DailyData, MonthlyData, RealtimeData, StationData

_LOGGER = logging.getLogger(__name__)

class MeteobridgeSQLDatabaseConnectionError(Exception):
    """Cannot connect to database."""


class MeteobridgeSQLDataError(Exception):
    """Cannot lookup data in the database."""


class MeteobridgeSQL:
    """Class that interfaces with a MySQL database, with weather data supplied by Meteobridge."""

    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        database: str,
        port: int = 3306,
    ) -> None:
        """Initialize the connection."""
        self._host = host
        self._user = user
        self._password = password
        self._database = database
        self._port = port

        self._weatherdb = None
        self._weather_cursor = None

    def initialize(self) -> None:
        """Initialize the connection."""
        try:
            self._weatherdb = mysql.connector.connect(
                host=self._host,
                user=self._user,
                password=self._password,
                database=self._database,
                port=self._port,
            )
        except mysql.connector.Error as err:
            raise MeteobridgeSQLDatabaseConnectionError(f"Failed to connect to the database: {err.msg}")

        self._weather_cursor = self._weatherdb.cursor()

    async def async_init(self) -> None:
        """Initialize the connection."""
        try:
            self._weatherdb = mysql.connector.connect(
                host=self._host,
                user=self._user,
                password=self._password,
                database=self._database,
                port=self._port,
            )
        except mysql.connector.Error as err:
            raise MeteobridgeSQLDatabaseConnectionError(f"Failed to connect to the database: {err.msg}")

        self._weather_cursor = self._weatherdb.cursor()

    async def async_disconnect(self) -> None:
        """Disconnect from the database."""
        if self._weather_cursor is not None:
            self._weather_cursor.close()
        if self._weatherdb is not None:
            self._weatherdb.close()

    async def async_get_realtime_data(self, id: str) -> RealtimeData:
        """Get the latest data from the database."""

        try:
            self._weather_cursor.execute(
                f"SELECT * FROM realtime_data WHERE ID = '{id}'"
            )
            result = self._weather_cursor.fetchone()
        except mysql.connector.Error as err:
            raise MeteobridgeSQLDataError(f"Failed to lookup data in the database: {err.msg}")

        return RealtimeData(*result)

    async def async_get_station_data(self, id: str) -> StationData:
        """Get station data from the database."""

        try:
            self._weather_cursor.execute(
                f"SELECT ID, mb_ip, mb_swversion, mb_buildnum, mb_platform, mb_station, mb_stationname FROM realtime_data WHERE ID = '{id}'"
            )
            result = self._weather_cursor.fetchone()
        except mysql.connector.Error as err:
            raise MeteobridgeSQLDataError(f"Failed to lookup data in the database: {err.msg}")

        return StationData(*result)


    async def async_get_forecast(self, hourly: bool=False) -> any:
        """Get the latest forecast."""

        result_array = []
        if hourly:
            try:
                self._weather_cursor.execute(
                    "SELECT* FROM forecast_hourly WHERE `datetime` >= NOW() LIMIT 48;"
                )
                result = self._weather_cursor.fetchall()
                for row in result:
                    result_array.append(ForecastHourly(*row))
            except mysql.connector.Error as err:
                raise MeteobridgeSQLDataError(f"Failed to lookup hourly forecast in the database: {err.msg}")
        else:
            try:
                self._weather_cursor.execute(
                    "SELECT* FROM forecast_daily;"
                )
                result = self._weather_cursor.fetchall()
                for row in result:
                    result_array.append(ForecastDaily(*row))
            except mysql.connector.Error as err:
                raise MeteobridgeSQLDataError(f"Failed to lookup daily forecast in the database: {err.msg}")

        return result_array


    async def async_get_minute_data(self, interval: str = '24') -> any:
        """Get data from the Minute Data table."""

        result_array = []
        try:
            self._weather_cursor.execute(
                f"SELECT * FROM viewMinuteData WHERE `logdate` > NOW() - INTERVAL {interval} HOUR;"
            )
            result = self._weather_cursor.fetchall()
            for row in result:
                result_array.append(MinuteData(*row))
        except mysql.connector.Error as err:
            raise MeteobridgeSQLDataError(f"Failed to lookup data from the minute_data table in the database: {err.msg}")

        return result_array

    async def async_get_daily_data(self, interval: str = '31') -> any:
        """Get data from the Daily Data table."""

        result_array = []
        try:
            self._weather_cursor.execute(
                f"SELECT * FROM viewDailyData WHERE `logdate` > NOW() - INTERVAL {interval} DAY;"
            )
            result = self._weather_cursor.fetchall()
            for row in result:
                result_array.append(DailyData(*row))
        except mysql.connector.Error as err:
            raise MeteobridgeSQLDataError(f"Failed to lookup data from the daily_data table in the database: {err.msg}")

        return result_array

    async def async_get_monthly_data(self, interval: str = '1') -> any:
        """Get data from the Monthly Data table."""

        result_array = []
        try:
            self._weather_cursor.execute(
                f"SELECT * FROM monthly_data WHERE `logdate` > NOW() - INTERVAL {interval} YEAR;"
            )
            result = self._weather_cursor.fetchall()
            for row in result:
                result_array.append(MonthlyData(*row))
        except mysql.connector.Error as err:
            raise MeteobridgeSQLDataError(f"Failed to lookup data from the monthly_data table in the database: {err.msg}")

        return result_array

