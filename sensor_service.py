import random

from api.button_pb2 import SensorState, SensorStates
from utils import config


async def make_sensor_state(id: int) -> SensorState:
    if id < 0 or id > int(config['SENSOR']['AMOUNT_STATES']) - 1:
        raise ValueError(f"Id must be in more than 0 and less than {int(config['SENSOR']['AMOUNT_STATES'])}")

    sensor_state = SensorState()
    sensor_state.id = id
    sensor_state.native_value = random.randint(0, int(config['SENSOR']['MAX_NATIVE_VALUE']))
    sensor_state.pressed = bool(random.getrandbits(1))

    return sensor_state


async def make_sensor_shelf(id: int) -> SensorStates:
    if id < 0 or id > int(config['SENSOR']['AMOUNT_SHELVES']) - 1:
        raise ValueError(f"Id must be in more than 0 and less than {int(config['SENSOR']['AMOUNT_SHELVES'])}")

    sensor_states = SensorStates()
    sensor_states.shelf = id
    sensor_states.sensor_id = id
    for sensor_id in range(int(config['SENSOR']['AMOUNT_STATES'])):
        sensor_states.states.append(await make_sensor_state(sensor_id))

    return sensor_states
