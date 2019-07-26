from sensor_service import make_sensor_state, make_sensor_shelf
import pytest

from utils import config


@pytest.mark.asyncio
async def test__make_sensor_state__create():
    TESTED_ID = int(config['SENSOR']['AMOUNT_STATES']) - 1

    sensor_state = await make_sensor_state(TESTED_ID)
    assert TESTED_ID == sensor_state.id


@pytest.mark.asyncio
async def test__make_sensor_state__wrong_id():
    TESTED_ID = int(config['SENSOR']['AMOUNT_STATES'])

    with pytest.raises(ValueError):
        await make_sensor_state(TESTED_ID)

    with pytest.raises(ValueError):
        await make_sensor_state(-TESTED_ID)


@pytest.mark.asyncio
async def test__make_sensor_shelf__create():
    TESTED_ID = int(config['SENSOR']['AMOUNT_SHELVES']) - 1
    AMOUNT_STATES = int(config['SENSOR']['AMOUNT_STATES'])

    sensor_states = await make_sensor_shelf(TESTED_ID)

    assert TESTED_ID == sensor_states.shelf
    assert TESTED_ID == sensor_states.sensor_id
    assert AMOUNT_STATES == len(sensor_states.states)


@pytest.mark.asyncio
async def test__make_sensor_shelf__wrong_id():
    TESTED_ID = int(config['SENSOR']['AMOUNT_SHELVES'])

    with pytest.raises(ValueError):
        await make_sensor_shelf(TESTED_ID)

    with pytest.raises(ValueError):
        await make_sensor_shelf(-TESTED_ID)
