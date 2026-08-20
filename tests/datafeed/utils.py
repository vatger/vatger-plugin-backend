from datetime import UTC, datetime

from datafeed.datafeed import ControllerModel, PilotModel


def make_pilot_flight_plan(**overrides) -> PilotModel.FlightPlanModel:
    defaults = {
        "flight_rules": "I",
        "aircraft": "B738",
        "aircraft_faa": "B738/L",
        "aircraft_short": "B738",
        "departure": "EDDF",
        "arrival": "EGLL",
        "alternate": "EGLC",
        "deptime": "",
        "enroute_time": "",
        "fuel_time": "",
        "remarks": "",
        "route": "",
        "revision_id": 1,
        "assigned_transponder": "1234",
    }
    defaults.update(overrides)
    return PilotModel.FlightPlanModel(**defaults)


def make_pilot(flightplan: PilotModel.FlightPlanModel | None = None, **overrides) -> PilotModel:
    if not flightplan:
        flightplan = make_pilot_flight_plan()

    defaults = {
        "cid": 1234567,
        "name": "Name",
        "callsign": "DLH123",
        "server": "Germany",
        "pilot_rating": 0,
        "military_rating": 0,
        "latitude": 50.0,
        "longitude": 8.0,
        "altitude": 35000,
        "groundspeed": 450,
        "transponder": "1234",
        "heading": 270,
        "qnh_i_hg": 29.92,
        "qnh_mb": 1013,
        "flight_plan": flightplan,
        "logon_time": datetime.now(UTC),
        "last_updated": datetime.now(UTC),
    }
    defaults.update(overrides)
    return PilotModel(**defaults)


def make_controller(**overrides) -> ControllerModel:
    now = datetime.now(UTC)

    data = {
        "cid": 1000001,
        "name": "Max Mustermann",
        "callsign": "EDDF_APP",
        "frequency": "120.800",
        "facility": 5,
        "rating": 5,
        "server": "EDDF",
        "visual_range": 200,
        "text_atis": None,
        "logon_time": now,
        "last_updated": now,
    }

    data.update(overrides)
    return ControllerModel.model_validate(data)
