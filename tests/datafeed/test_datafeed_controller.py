import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.guards import get_user
from containers.dependencies import DependencyContainer
from datafeed.api.datafeed_controller import router
from datafeed.api.datafeed_responses import ControllerResponse, PilotResponse
from datafeed.datafeed import ControllerModel
from tests.datafeed.utils import make_pilot
from tests.mocks.repositories.mock_datafeed_repository import MockDatafeedRepository
from users.user import User

pytestmark = pytest.mark.unit


@pytest.fixture
def datafeed_repo():
    return MockDatafeedRepository()


def make_user(cid: int = 1234567, user_id: uuid.UUID | None = None) -> User:
    if not user_id:
        user_id = uuid.uuid4()

    return User(
        id=user_id,
        cid=cid,
        name="",
        rating="S2",
        access=True,
    )


@pytest.fixture
def client(datafeed_repo):
    app = FastAPI()
    app.include_router(router)

    container = DependencyContainer()
    container.wire(modules=["datafeed.api.datafeed_controller"])
    container.datafeed_container.datafeed_repository.override(datafeed_repo)

    def mock_get_user() -> User:
        return make_user()  # match your make_pilot default

    app.dependency_overrides[get_user] = mock_get_user

    with TestClient(app) as c:
        yield c

    container.reset_override()


def test_returns_pilot_data_for_authenticated_user(client, datafeed_repo):
    datafeed_repo.add_pilot(make_pilot(cid=1234567))

    response = client.get("/datafeed/user/pilot")

    assert response.status_code == 200
    assert response.json()["cid"] == 1234567
    assert response.json()["callsign"] == "DLH123"
    assert response.json()["name"] is not None
    assert response.json()["transponder"] is not None
    assert response.json()["server"] is not None
    assert response.json()["flight_plan"]["aircraft_short"] is not None


def test_returns_correct_pilot_fields(client, datafeed_repo):
    datafeed_repo.add_pilot(make_pilot(cid=1234567, callsign="DLH124"))

    response = client.get("/datafeed/user/pilot")
    body = response.json()

    assert body["cid"] == 1234567
    assert body["callsign"] == "DLH124"
    assert body["altitude"] == 35000
    assert body["groundspeed"] == 450
    assert body["heading"] == 270


def test_returns_null_when_user_has_no_active_pilot(client, datafeed_repo):
    response = client.get("/datafeed/user/pilot")

    assert response.status_code == 200
    assert response.json() is None


def test_returns_null_when_different_pilot_is_online(client, datafeed_repo):
    datafeed_repo.add_pilot(make_pilot(cid=9999999))

    response = client.get("/datafeed/user/pilot")

    assert response.status_code == 200
    assert response.json() is None


def test_response_is_valid_pilot_dto(client, datafeed_repo):
    datafeed_repo.add_pilot(make_pilot(cid=1234567))

    response = client.get("/datafeed/user/pilot")

    assert response.status_code == 200
    dto = PilotResponse(**response.json())
    assert dto.cid == 1234567


def test_response_controller(client, datafeed_repo):
    user = make_user()

    datafeed_repo.add_controller(
        ControllerModel(
            cid=user.cid,
            name="Test",
            callsign="EDDF_TWR",
            frequency="123.450",
            facility=4,
            rating=3,
            server="Germany",
            visual_range=50,
            logon_time=datetime.now(UTC),
            last_updated=datetime.now(UTC),
        )
    )

    response = client.get("/datafeed/user/controller")

    assert response.status_code == 200
    dto = ControllerResponse(**response.json())
    assert dto.cid == user.cid
    assert dto.facility == 4
