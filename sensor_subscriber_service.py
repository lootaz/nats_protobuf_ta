import asyncio
import logging
import sys
from typing import Dict

import nats
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from asyncqt import QEventLoop

from api.button_pb2 import SensorStates
from utils import config
from widgets.sensor_shelf_widget import SensorShelfWidget

logging.basicConfig(format="%(asctime)s[%(levelname)s]: %(message)s",
                    level=logging.INFO)
logger = logging.getLogger("publisher")


class SensorSubscriberWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs) -> None:
        super(SensorSubscriberWidget, self).__init__(parent, *args, **kwargs)

        self.client: nats.aio.client.Client = nats.aio.client.Client()

        self.sensor_shelves: Dict[int, SensorShelfWidget] = {}

        vbx_main = QVBoxLayout()
        self.setLayout(vbx_main)

        self.resize(400, 300)

        self.subject = config['COMMON']['SUBJECT']
        self.nats_url = config['COMMON']['NATS_URL']

        self.setWindowTitle("SmaSS Subscriber")

    def render_view(self):
        layout = self.layout()

        for sensor_shelf in self.sensor_shelves.values():
            layout.addWidget(sensor_shelf)

    async def receive(self) -> None:
        await self.client.connect(self.nats_url)

        async def callback_(msg):
            logger.info("Message received!")

            sensor_states = SensorStates()
            sensor_states.ParseFromString(msg.data)

            sensor_shelf_widget = self.sensor_shelves.get(sensor_states.shelf, SensorShelfWidget())
            sensor_shelf_widget.fill_from_sensor_states(sensor_states)
            self.sensor_shelves[sensor_states.shelf] = sensor_shelf_widget

            self.render_view()

        await self.client.subscribe(self.subject, cb=callback_)

        future = asyncio.Future()
        await asyncio.gather(future)

    def close(self) -> None:
        self.client.close()


if __name__ == '__main__':
    if (sys.version_info[0], sys.version_info[1]) < (3, 7):
        raise Exception("Required Python 3.7+")

    app = QApplication(sys.argv)
    loop = QEventLoop(app)

    asyncio.set_event_loop(loop)

    wgt = SensorSubscriberWidget()
    wgt.show()

    try:
        with loop:
            sys.exit(loop.run_until_complete(wgt.receive()))
    except (Exception, SystemExit, KeyboardInterrupt):
        wgt.close()
