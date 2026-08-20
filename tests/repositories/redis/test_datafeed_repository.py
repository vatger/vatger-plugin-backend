import fakeredis
import pytest

from datafeed.datafeed import ControllerModel, DatafeedModel, PilotModel
from repositories.redis.datafeed_repository import RedisDatafeedRepository
from tests.datafeed.utils import make_controller, make_pilot


@pytest.fixture
def redis_client():
    yield fakeredis.aioredis.FakeRedis()


@pytest.fixture
def repository(redis_client):
    return RedisDatafeedRepository(redis_client)


def make_feed(
    pilots: list[PilotModel] | None = None,
    controllers: list[ControllerModel] | None = None,
) -> DatafeedModel:
    return DatafeedModel.model_validate({
        "pilots": pilots or [],
        "controllers": controllers or [],
    })


@pytest.mark.asyncio
async def test_update_stores_callsigns(repository):
    await repository.update(
        make_feed(
            pilots=[
                make_pilot(callsign="ABC123", cid=9000001),
                make_pilot(callsign="XYZ789", cid=9000002),
            ]
        )
    )

    assert await repository.has_pilot("ABC123") is True
    assert await repository.has_pilot("XYZ789") is True
    assert await repository.has_pilot("NON_EXISTING") is False


@pytest.mark.asyncio
async def test_get_pilot_by_callsign_returns_model(repository):
    await repository.update(
        make_feed(
            pilots=[
                make_pilot(callsign="ABC123", cid=9000001, latitude=50.0, longitude=8.0),
            ]
        )
    )

    pilot = await repository.get_pilot_by_callsign("ABC123")

    assert isinstance(pilot, PilotModel)
    assert pilot.callsign == "ABC123"
    assert pilot.cid == 9000001
    pytest.approx(pilot.latitude, 50.0)
    pytest.approx(pilot.longitude, 8.0)


@pytest.mark.asyncio
async def test_get_pilot_by_callsign_missing_returns_none(repository):
    await repository.update(make_feed())

    assert await repository.get_pilot_by_callsign("MISSING") is None


@pytest.mark.asyncio
async def test_get_pilot_by_cid_returns_model(repository):
    await repository.update(
        make_feed(
            pilots=[
                make_pilot(callsign="ABC123", cid=9000001),
            ]
        )
    )

    pilot = await repository.get_pilot_by_cid(9000001)

    assert isinstance(pilot, PilotModel)
    assert pilot.callsign == "ABC123"
    assert pilot.cid == 9000001


@pytest.mark.asyncio
async def test_get_pilot_by_cid_missing_returns_none(repository):
    await repository.update(make_feed())

    assert await repository.get_pilot_by_cid(9999999) is None


@pytest.mark.asyncio
async def test_update_removes_old_callsigns(repository):
    await repository.update(
        make_feed(
            pilots=[
                make_pilot(callsign="OLD1", cid=9000001),
                make_pilot(callsign="OLD2", cid=9000002),
            ]
        )
    )

    await repository.update(
        make_feed(
            pilots=[
                make_pilot(callsign="NEW1", cid=9000003),
            ]
        )
    )

    assert await repository.has_pilot("OLD1") is False
    assert await repository.has_pilot("OLD2") is False
    assert await repository.has_pilot("NEW1") is True


@pytest.mark.asyncio
async def test_old_pilot_data_removed(repository):
    await repository.update(make_feed(pilots=[make_pilot(callsign="OLD1", cid=9000001)]))
    await repository.update(make_feed())

    assert await repository.get_pilot_by_callsign("OLD1") is None


@pytest.mark.asyncio
async def test_old_pilot_cid_index_removed(repository):
    await repository.update(make_feed(pilots=[make_pilot(callsign="OLD1", cid=9000001)]))
    await repository.update(make_feed())

    assert await repository.get_pilot_by_cid(9000001) is None


@pytest.mark.asyncio
async def test_update_stores_controllers(repository):
    await repository.update(
        make_feed(
            controllers=[
                make_controller(callsign="EDDF_APP", cid=1000001),
                make_controller(callsign="EDDF_TWR", cid=1000002),
            ]
        )
    )

    assert await repository.has_controller("EDDF_APP") is True
    assert await repository.has_controller("EDDF_TWR") is True
    assert await repository.has_controller("EDDF_GND") is False


@pytest.mark.asyncio
async def test_get_controller_by_callsign_returns_model(repository):
    await repository.update(
        make_feed(
            controllers=[
                make_controller(callsign="EDDF_APP", cid=1000001, frequency="120.800"),
            ]
        )
    )

    controller = await repository.get_controller_by_callsign("EDDF_APP")

    assert isinstance(controller, ControllerModel)
    assert controller.callsign == "EDDF_APP"
    assert controller.cid == 1000001
    assert controller.frequency == "120.800"


@pytest.mark.asyncio
async def test_get_controller_by_callsign_missing_returns_none(repository):
    await repository.update(make_feed())

    assert await repository.get_controller_by_callsign("EDDF_APP") is None


@pytest.mark.asyncio
async def test_get_controller_by_cid_returns_model(repository):
    await repository.update(
        make_feed(
            controllers=[
                make_controller(callsign="EDDF_APP", cid=1000001),
            ]
        )
    )

    controller = await repository.get_controller_by_cid(1000001)

    assert isinstance(controller, ControllerModel)
    assert controller.callsign == "EDDF_APP"
    assert controller.cid == 1000001


@pytest.mark.asyncio
async def test_get_controller_by_cid_missing_returns_none(repository):
    await repository.update(make_feed())

    assert await repository.get_controller_by_cid(9999999) is None


@pytest.mark.asyncio
async def test_update_removes_old_controllers(repository):
    await repository.update(
        make_feed(
            controllers=[
                make_controller(callsign="EDDF_APP", cid=1000001),
                make_controller(callsign="EDDF_TWR", cid=1000002),
            ]
        )
    )

    await repository.update(
        make_feed(
            controllers=[
                make_controller(callsign="EDDF_GND", cid=1000003),
            ]
        )
    )

    assert await repository.has_controller("EDDF_APP") is False
    assert await repository.has_controller("EDDF_TWR") is False
    assert await repository.has_controller("EDDF_GND") is True


@pytest.mark.asyncio
async def test_old_controller_data_removed(repository):
    await repository.update(
        make_feed(
            controllers=[
                make_controller(callsign="EDDF_APP", cid=1000001),
            ]
        )
    )
    await repository.update(make_feed())

    assert await repository.get_controller_by_callsign("EDDF_APP") is None


@pytest.mark.asyncio
async def test_old_controller_cid_index_removed(repository):
    await repository.update(
        make_feed(
            controllers=[
                make_controller(callsign="EDDF_APP", cid=1000001),
            ]
        )
    )
    await repository.update(make_feed())

    assert await repository.get_controller_by_cid(1000001) is None


# --- Cross-entity tests ---


@pytest.mark.asyncio
async def test_pilots_and_controllers_are_independent(repository):
    await repository.update(
        make_feed(
            pilots=[make_pilot(callsign="ABC123", cid=9000001)],
            controllers=[make_controller(callsign="EDDF_APP", cid=1000001)],
        )
    )

    assert await repository.has_pilot("ABC123") is True
    assert await repository.has_controller("EDDF_APP") is True

    await repository.update(make_feed(pilots=[make_pilot(callsign="ABC123", cid=9000001)]))

    assert await repository.has_pilot("ABC123") is True
    assert await repository.has_controller("EDDF_APP") is False
