from datetime import datetime
from enum import IntEnum
from typing import Literal

from pydantic import BaseModel


class PilotResponse(BaseModel):
    class FlightPlanResponse(BaseModel):
        flight_rules: Literal["I", "V"]
        aircraft: str
        aircraft_faa: str
        aircraft_short: str
        departure: str
        arrival: str
        alternate: str
        deptime: str
        enroute_time: str
        fuel_time: str
        remarks: str
        route: str
        revision_id: int
        assigned_transponder: str

    cid: int
    name: str
    callsign: str
    server: str
    pilot_rating: int
    military_rating: int
    latitude: float
    longitude: float
    altitude: int
    groundspeed: int
    transponder: str
    heading: int
    qnh_i_hg: float
    qnh_mb: int
    flight_plan: FlightPlanResponse | None = None
    logon_time: datetime
    last_updated: datetime


class ControllerResponse(BaseModel):
    class FacilityResponse(IntEnum):
        OBS = 0
        FSS = 1
        DEL = 2
        GND = 3
        TWR = 4
        APP = 5
        CTR = 6

    cid: int
    name: str
    callsign: str
    frequency: str
    facility: FacilityResponse
    rating: int
    server: str
    visual_range: int
    text_atis: list[str] | None = None
    logon_time: datetime
    last_updated: datetime
