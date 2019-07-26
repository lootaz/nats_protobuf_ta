import sys
from typing import Optional, Dict

from PyQt5.QtWidgets import QHBoxLayout, QWidget

from api.button_pb2 import SensorStates
from widgets.sensor_widget import SensorWidget


class SensorShelfWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.shelf: Optional[int] = None
        self.sensor_id: Optional[int] = None
        self.sensors: Dict[int, SensorWidget] = {}

        hbx_main = QHBoxLayout()
        hbx_main.setSpacing(0)
        self.setLayout(hbx_main)

    def render_view(self) -> None:
        layout = self.layout()

        for sensor in self.sensors.values():
            layout.addWidget(sensor)

        self.setStyleSheet("background-color: blue;")

    def fill_from_sensor_states(self, sensor_states: SensorStates) -> None:
        self.shelf = sensor_states.shelf
        self.sensor_id = sensor_states.sensor_id

        for sensor_state in sensor_states.states:
            sensor = self.sensors.get(sensor_state.id)
            if not sensor:
                self.sensors[sensor_state.id] = SensorWidget()
                sensor = self.sensors.get(sensor_state.id)

            sensor.fill_from_sensor_state(sensor_state)

        self.render_view()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    sss = SensorStates()
    sss.shelf = 1
    sss.sensor_id = 1

    sensor = sss.states.add()
    sensor.id = 0
    sensor.native_value = 10
    sensor.pressed = True

    sensor = sss.states.add()
    sensor.id = 7
    sensor.native_value = 70
    sensor.pressed = False

    wgt = SensorShelfWidget()
    wgt.fill_from_sensor_states(sss)
    wgt.show()

    sys.exit(app.exec_())

    pass
