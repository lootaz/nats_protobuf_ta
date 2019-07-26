from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QFrame

from api.button_pb2 import SensorState


class SensorWidget(QFrame):
    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.id: Optional[int] = None
        self.native_value: Optional[int] = None
        self.pressed: bool = False

        self.lbl_id = QLabel()
        self.lbl_id.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.lbl_value = QLabel()
        self.lbl_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        vbx_main = QVBoxLayout()
        vbx_main.setSpacing(0)
        vbx_main.addWidget(self.lbl_id, alignment=Qt.AlignHCenter)
        vbx_main.addWidget(self.lbl_value, alignment=Qt.AlignHCenter)

        self.setLayout(vbx_main)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_id(self, id: int) -> None:
        self.id = id

    def set_native_value(self, value: int) -> None:
        self.native_value = value

    def set_pressed(self, pressed: bool) -> None:
        self.pressed = pressed

    def fill_from_sensor_state(self, sensor_state: SensorState) -> None:
        self.set_id(sensor_state.id)
        self.set_native_value(sensor_state.native_value)
        self.set_pressed(sensor_state.pressed)

        self.render_view()

    def render_view(self) -> None:
        stylesheet_str = f"""
            QFrame {{
                background-color: {"red" if self.pressed else "lightGreen"};
            }}
        """

        self.setStyleSheet(stylesheet_str)

        self.lbl_id.setText(str(self.id))
        self.lbl_value.setText(str(self.native_value))
