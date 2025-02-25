import random
import sys

from httpx_ws import connect_ws
from pycrdt import Doc, Text
from pyqt_crdt import WebsocketProvider
from PySide6 import QtCore, QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

        self.greeting = Text()
        self.doc = Doc({"greeting": self.greeting})

        def callback(event):
            self.text.setText(str(self.greeting))

        self.greeting.observe(callback)

    @QtCore.Slot()
    def magic(self):
        with self.doc.transaction():
            self.greeting.clear()
            self.greeting += random.choice(self.hello)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    with connect_ws("http://localhost:1234/my_room") as websocket:
        websocket_provider = WebsocketProvider(widget.doc, websocket)
        websocket_provider.start()

        timer = QtCore.QTimer()
        timer.timeout.connect(websocket_provider.run)
        timer.start()

        sys.exit(app.exec())
