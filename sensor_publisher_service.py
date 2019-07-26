import asyncio
import logging
import sys

import nats

from sensor_service import make_sensor_shelf
from utils import config

logging.basicConfig(format="%(asctime)s[%(levelname)s]: %(message)s",
                    level=logging.INFO)
logger = logging.getLogger("publisher")


class SensorPublisherService:
    def __init__(self) -> None:
        self.client = nats.aio.client.Client()

        self.amount_shelf = int(config['SENSOR']['AMOUNT_SHELVES'])
        self.subject = config['COMMON']['SUBJECT']
        self.nats_url = config['COMMON']['NATS_URL']

        self.message_period_sec = int(config['PUBLISHER']['MESSAGE_PERIOD_SEC'])

    async def send_sensor_shelves(self) -> None:

        for shelf_id in range(self.amount_shelf):
            sensor_states = await make_sensor_shelf(shelf_id)
            data = sensor_states.SerializeToString()

            await self.client.publish(self.subject, data)

    async def send(self) -> None:
        await self.client.connect(servers=[self.nats_url])

        while True:
            await self.send_sensor_shelves()
            logger.info("...message sent")

            await asyncio.sleep(self.message_period_sec)

    def close(self) -> None:
        self.client.close()


if __name__ == '__main__':
    if (sys.version_info[0], sys.version_info[1]) < (3, 7):
        raise Exception("Required Python 3.7+")

    service = SensorPublisherService()
    try:
        asyncio.run(service.send())
    except (Exception, SystemExit, KeyboardInterrupt):
        service.close()
