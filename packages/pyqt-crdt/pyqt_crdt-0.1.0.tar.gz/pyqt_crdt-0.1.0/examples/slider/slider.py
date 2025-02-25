import sys

from httpx_ws import connect_ws
from pycrdt import Doc, Map
from pyqt_crdt import WebsocketProvider
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QSlider, QWidget


class MyWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(320, 150)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setGeometry(10, 10, 300, 40)
        self.slider.valueChanged.connect(self.slider_value_changed)

        self.button = QPushButton("Reset", self)
        self.button.setGeometry(10, 50, 100, 35)
        self.button.clicked.connect(self.button_reset_value)

        self.label = QLabel(self)
        self.label.setGeometry(250, 50, 50, 35)

        self.map = Map()
        self.doc = Doc({"map": self.map})
        self.map.observe(self.shared_value_changed)


    def shared_value_changed(self, event):
        value = self.map["value"]
        self.slider.setValue(value)
        self.label.setText(str(int(value)))

    def slider_value_changed(self, value):
        #with self.doc.transaction(origin="slider"):
        try:
            self.map["value"] = value
        except:
            pass

    def button_reset_value(self):
        self.map["value"] = 0


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    with connect_ws("http://localhost:1234/my_room") as websocket:
        websocket_provider = WebsocketProvider(widget.doc, websocket)
        websocket_provider.start()

        timer = QTimer()
        timer.timeout.connect(websocket_provider.run)
        timer.start()

        sys.exit(app.exec())
