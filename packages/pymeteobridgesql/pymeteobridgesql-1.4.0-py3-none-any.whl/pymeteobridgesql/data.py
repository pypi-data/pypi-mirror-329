"""This module describes dataclasses used by pymeteobridgesql."""

from __future__ import annotations

from dataclasses import dataclass
import datetime
import math

@dataclass(frozen=True)
class RealtimeData:
    ID: str
    temperature: float
    tempmax: float
    tempmin: float
    windchill: float
    pm1: float
    pm25: float
    pm10: float
    heatindex: float
    temp15min: float
    humidity: int
    windspeedavg: float
    windgust: float
    dewpoint: float
    rainrate: float
    raintoday: float
    rainyesterday: float
    windbearing: int
    windbearingavg10: int
    windbearingdavg: int
    beaufort: int
    sealevelpressure: float
    uv: float
    uvdaymax: float
    solarrad: float
    solarraddaymax: float
    pressuretrend: float
    mb_ip: str
    mb_swversion: str
    mb_buildnum: str
    mb_platform: str
    mb_station: str
    mb_stationname: str
    elevation: int
    description: str
    icon: str
    conditions: str

    @property
    def absolute_humidity(self) -> float:
        """Aboslute Humidity (g.m-3)."""
        if self.temperature is None or self.humidity is None:
            return None

        kelvin = self.temperature + 273.16
        humidity = self.humidity / 100
        return (1320.65 / kelvin) * humidity * (10 ** ((7.4475 * (kelvin - 273.14)) / (kelvin - 39.44)))

    @property
    def aqi(self) -> int:
        """Air Quality Index."""
        return aqi_from_pm25(self.pm25)

    @property
    def beaufort_description(self) -> str:
        """Beaufort Textual Description."""

        if self.windspeedavg is None:
            return None

        mapping_text = {
            "32.7": "hurricane",
            "28.5": "violent_storm",
            "24.5": "storm",
            "20.8": "strong_gale",
            "17.2": "fresh_gale",
            "13.9": "moderate_gale",
            "10.8": "strong_breeze",
            "8.0": "fresh_breeze",
            "5.5": "moderate_breeze",
            "3.4": "gentle_breeze",
            "1.6": "light_breeze",
            "0.3": "light_air",
            "-1": "calm",
        }

        for key, value in mapping_text.items():
            if self.windspeedavg > float(key):
                return value
        return None

    @property
    def cloud_base(self) -> float:
        """Cloud Base (km)."""
        if self.elevation is None or self.temperature is None or self.dewpoint is None:
            return None

        return (self.temperature - self.dewpoint) * 126 + self.elevation

    @property
    def feels_like_temperature(self) -> float:
        """Calculate feels like temperature using windchill and heatindex."""
        if self.windchill is not None and self.heatindex is not None and self.temperature is not None and self.humidity is not None and self.windspeedavg is not None:
            if self.temperature > 26.7 and self.humidity > 40:
                return self.heatindex
            if self.temperature < 10 and self.windspeedavg > 4.8:
                return self.windchill
            return self.temperature
        return None

    @property
    def freezing_altitude(self) -> float:
        """Freezing Altitude."""
        if self.elevation is None or self.temperature is None:
            return None

        _freezing_line = (192 * self.temperature) + self.elevation
        return 0 if _freezing_line < 0 else _freezing_line

    @property
    def pressuretrend_text(self) -> str:
        """Converts the pressure trend to text."""
        if self.pressuretrend is None:
            return None

        if self.pressuretrend > 0:
            return "rising"
        if self.pressuretrend < 0:
            return "falling"
        return "steady"

    @property
    def uv_description(self) -> str:
        """UV value description."""
        if self.uv is None:
            return None

        mapping_text = {
            "10.5": "extreme",
            "7.5": "very-high",
            "5.5": "high",
            "2.8": "moderate",
            "0": "low",
        }

        for key, value in mapping_text.items():
            if self.uv >= float(key):
                return value
        return None

    @property
    def visibility(self) -> float:
        """Visibility (km)."""
        if self.elevation is None or self.temperature is None or self.dewpoint is None:
            return None

        _elevation_min = float(2)
        if self.elevation > 2:
            _elevation_min = self.elevation

        _max_visibility = float(3.56972 * math.sqrt(_elevation_min))
        _percent_reduction_a = float((1.13 * abs(self.temperature - self.dewpoint) - 1.15) / 10)
        if _percent_reduction_a > 1:
            _percent_reduction = float(1)
        elif _percent_reduction_a < 0.025:
            _percent_reduction = 0.025
        else:
            _percent_reduction = _percent_reduction_a

        return float(_max_visibility * _percent_reduction)

    @property
    def wind_direction(self) -> str:
        """Calculates the wind direction from the wind bearing."""
        if self.windbearing is None:
            return None

        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = round(self.windbearing / 22.5) % 16
        return directions[index].lower()

    def to_dict(self):
        return {
            "ID": self.ID,
            "temperature": self.temperature,
            "tempmax": self.tempmax,
            "tempmin": self.tempmin,
            "windchill": self.windchill,
            "pm1": self.pm1,
            "pm25": self.pm25,
            "pm10": self.pm10,
            "heatindex": self.heatindex,
            "temp15min": self.temp15min,
            "humidity": self.humidity,
            "windspeedavg": self.windspeedavg,
            "windgust": self.windgust,
            "dewpoint": self.dewpoint,
            "rainrate": self.rainrate,
            "raintoday": self.raintoday,
            "rainyesterday": self.rainyesterday,
            "windbearing": self.windbearing,
            "beaufort": self.beaufort,
            "sealevelpressure": self.sealevelpressure,
            "uv": self.uv,
            "uvdaymax": self.uvdaymax,
            "solarrad": self.solarrad,
            "solarraddaymax": self.solarraddaymax,
            "pressuretrend": self.pressuretrend,
            "mb_ip": self.mb_ip,
            "mb_swversion": self.mb_swversion,
            "mb_buildnum": self.mb_buildnum,
            "mb_platform": self.mb_platform,
            "mb_station": self.mb_station,
            "mb_stationname": self.mb_stationname,
            "elevation": self.elevation,
            "description": self.description,
            "icon": self.icon,
            "conditions": self.conditions,
            "absolute_humidity": self.absolute_humidity,
            "aqi": self.aqi,
            "beaufort_description": self.beaufort_description,
            "cloud_base": self.cloud_base,
            "feels_like_temperature": self.feels_like_temperature,
            "freezing_altitude": self.freezing_altitude,
            "pressuretrend_text": self.pressuretrend_text,
            "uv_description": self.uv_description,
            "visibility": self.visibility,
            "wind_direction": self.wind_direction,
        }

@dataclass(frozen=True)
class ForecastHourly:
    hour_num: int
    datetime: datetime.datetime
    temperature: float
    apparent_temperature: float
    humidity: int
    description: str
    icon: str
    precipitation_probability: int
    precipitation: float
    pressure: float
    wind_bearing: int
    wind_speed: float
    wind_gust: float
    uv_index: float
    visibility: float

    def to_dict(self):
        return {
            "hour_num": self.hour_num,
            "datetime": self.datetime,
            "temperature": self.temperature,
            "apparent_temperature": self.apparent_temperature,
            "humidity": self.humidity,
            "description": self.description,
            "icon": self.icon,
            "precipitation_probability": self.precipitation_probability,
            "precipitation": self.precipitation,
            "pressure": self.pressure,
            "wind_bearing": self.wind_bearing,
            "wind_speed": self.wind_speed,
            "wind_gust": self.wind_gust,
            "uv_index": self.uv_index,
            "visibility": self.visibility,
        }

@dataclass(frozen=True)
class ForecastDaily:
    day_num: int
    datetime: datetime.datetime
    temperature: float
    temp_low: float
    description: str
    icon: str
    precipitation_probability: int
    precipitation: float
    pressure: float
    sunriseepoch: int
    sunsetepoch: int
    wind_bearing: int
    wind_speed: float
    wind_gust: float
    conditions: str

    def to_dict(self):
        return {
            "day_num": self.day_num,
            "datetime": self.datetime,
            "temperature": self.temperature,
            "temp_low": self.temp_low,
            "description": self.description,
            "icon": self.icon,
            "precipitation_probability": self.precipitation_probability,
            "precipitation": self.precipitation,
            "pressure": self.pressure,
            "sunriseepoch": self.sunriseepoch,
            "sunsetepoch": self.sunsetepoch,
            "wind_bearing": self.wind_bearing,
            "wind_speed": self.wind_speed,
            "wind_gust": self.wind_gust,
            "conditions": self.conditions,
        }

@dataclass(frozen=True)
class StationData:
    ID: str
    mb_ip: str
    mb_swversion: str
    mb_buildnum: str
    mb_platform: str
    mb_station: str
    mb_stationname: str


@dataclass(frozen=True)
class MinuteData:
    logdate: datetime.datetime
    temperature: float
    wind_chill: float
    air_Quality_pm1: float
    air_Quality_pm10: float
    air_Quality_pm25: float
    heat_index: float
    humidity: int
    dewpoint: float
    rain_rate: float
    rain_day: float
    rain_hour: float
    wind_speed: float
    wind_gust: float
    wind_bearing: int
    pressure: float
    pressure_trend: float
    uv: float
    solar_radiation: float
    visibility: float

    def to_dict(self):
        return {
            "logdate": self.logdate,
            "temperature": self.temperature,
            "wind_chill": self.wind_chill,
            "air_Quality_pm1": self.air_Quality_pm1,
            "air_Quality_pm10": self.air_Quality_pm10,
            "air_Quality_pm25": self.air_Quality_pm25,
            "heat_index": self.heat_index,
            "humidity": self.humidity,
            "dewpoint": self.dewpoint,
            "rain_rate": self.rain_rate,
            "rain_day": self.rain_day,
            "rain_hour": self.rain_hour,
            "wind_speed": self.wind_speed,
            "wind_gust": self.wind_gust,
            "wind_bearing": self.wind_bearing,
            "pressure": self.pressure,
            "pressure_trend": self.pressure_trend,
            "uv": self.uv,
            "solar_radiation": self.solar_radiation,
            "visibility": self.visibility,
        }


@dataclass(frozen=True)
class DailyData:
    logdate: datetime.date
    temperature_low: float
    temperature_high: float
    humidity_low: int
    humidity_high: int
    rain_total: float
    wind_speed_max: float
    wind_speed_avg: float
    wind_direction_avg: int
    uvindex_max: float
    solar_radiation_max: float
    pressure_low: float
    pressure_high: float
    air_quality_low: float
    air_quality_high: float
    dewpoint_low: float
    dewpoint_high: float
    visibility_low: float
    visibility_high: float

    def to_dict(self):
        return {
            "logdate": self.logdate,
            "temperature_low": self.temperature_low,
            "temperature_high": self.temperature_high,
            "humidity_low": self.humidity_low,
            "humidity_high": self.humidity_high,
            "rain_total": self.rain_total,
            "wind_speed_max": self.wind_speed_max,
            "wind_speed_avg": self.wind_speed_avg,
            "wind_direction_avg": self.wind_direction_avg,
            "uvindex_max": self.uvindex_max,
            "solar_radiation_max": self.solar_radiation_max,
            "pressure_low": self.pressure_low,
            "pressure_high": self.pressure_high,
            "air_quality_low": self.air_quality_low,
            "air_quality_high": self.air_quality_high,
            "dewpoint_low": self.dewpoint_low,
            "dewpoint_high": self.dewpoint_high,
            "visibility_low": self.visibility_low,
            "visibility_high": self.visibility_high,
        }

@dataclass(frozen=True)
class MonthlyData:
    logdate: datetime.date
    temperature_low: float
    temperature_high: float
    humidity_low: int
    humidity_high: int
    rain_total: float
    wind_speed_max: float
    wind_speed_avg: float
    wind_direction_avg: int
    uvindex_max: float
    solar_radiation_max: float
    pressure_low: float
    pressure_high: float
    air_quality_low: float
    air_quality_high: float

    def to_dict(self):
        return {
            "logdate": self.logdate,
            "temperature_low": self.temperature_low,
            "temperature_high": self.temperature_high,
            "humidity_low": self.humidity_low,
            "humidity_high": self.humidity_high,
            "rain_total": self.rain_total,
            "wind_speed_max": self.wind_speed_max,
            "wind_speed_avg": self.wind_speed_avg,
            "wind_direction_avg": self.wind_direction_avg,
            "uvindex_max": self.uvindex_max,
            "solar_radiation_max": self.solar_radiation_max,
            "pressure_low": self.pressure_low,
            "pressure_high": self.pressure_high,
            "air_quality_low": self.air_quality_low,
            "air_quality_high": self.air_quality_high,
        }

def aqi_from_pm25(pm25: float) -> int:
    """Calculate the Air Quality Index from the PM2.5 value."""
    if pm25 is None:
        return None

    if pm25 > 500:
        return 500
    if pm25 < 0:
        return 0

    if pm25 > 350.5:
        return calcAQI(pm25, 500, 401, 500, 350.5)
    if pm25 > 250.5:
        return calcAQI(pm25, 400, 301, 350.4, 250.5)
    if pm25 > 150.5:
        return calcAQI(pm25, 300, 201, 250.4, 150.5)
    if pm25 > 55.5:
        return calcAQI(pm25, 200, 151, 150.4, 55.5)
    if pm25 > 35.5:
        return calcAQI(pm25, 150, 101, 55.4, 35.5)
    if pm25 > 12.1:
        return calcAQI(pm25, 100, 51, 35.4, 12.1)
    if pm25 > 0:
        return calcAQI(pm25, 50, 0, 12, 0)
    return 0

def calcAQI(pm25: float, ih: int, il: int, bph: int, bpl: int) -> float:
    """Calculate the Air Quality Index from the PM2.5 value."""
    if pm25 is None:
        return None

    _val1 = (ih - il)
    _val2 = (bph - bpl)
    _val3 = (pm25 - bpl)
    return float(_val1 / _val2 * _val3 + il)

