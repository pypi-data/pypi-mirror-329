import sys
from functools import partial
from uuid import uuid4

import anyio
from anyioutils import start_guest_run
from httpx_ws import aconnect_ws
from pycrdt import Array, Doc, Map, Text
from pycrdt_websocket import WebsocketProvider
from pycrdt_websocket.websocket import HttpxWebsocket
from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget

class AsyncHelper(QObject):

    class ReenterQtObject(QObject):
        def event(self, event):
            if event.type() == QEvent.Type.User + 1:
                event.fn()
                return True
            return False

    class ReenterQtEvent(QEvent):
        def __init__(self, fn):
            super().__init__(QEvent.Type(QEvent.Type.User + 1))
            self.fn = fn

    def __init__(self, entry):
        super().__init__()
        self.reenter_qt = self.ReenterQtObject()
        start_guest_run(
            entry,
            run_sync_soon_threadsafe=self.next_guest_run_schedule,
            done_callback=self.done_callback,
            backend="asyncio",
        )

    def next_guest_run_schedule(self, fn):
        QApplication.postEvent(self.reenter_qt, self.ReenterQtEvent(fn))

    def done_callback(self, outcome_):
        pass


class Notebook(QWidget):
    def __init__(self):
        super().__init__()

        self.doc = Doc()
        self.cells = self.doc.get("cells", type=Array)

        self.add_cell_button = QPushButton("Add cell")
        self.add_cell_button.clicked.connect(self.add_cell)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.add_cell_button)
        self.setLayout(self.layout)

        self.cells.observe_deep(self.cells_changed)

    def add_cell(self):
        cell = Map({
            "text": Text(),
            "id": uuid4().hex,
        })
        self.cells.append(cell)

    def delete_cell(self, cell_id):
        for idx, cell in enumerate(self.cells):
            if cell["id"] == cell_id:
                del self.cells[idx]
                return

    def my_text_edited(self, shared_text, new_text):
        with shared_text.doc.transaction():
            shared_text.clear()
            shared_text += new_text

    def cells_changed(self, events):
        for event in events:
            if event.path:
                idx, key = event.path
                cell = self.layout.itemAt(idx + 1)
                input_widget = cell.itemAt(0).widget()
                cursor_position = input_widget.cursorPosition()
                input_widget.setText(str(event.target))
                input_widget.setCursorPosition(cursor_position)
            else:
                row = 1
                for delta in event.delta:
                    row += delta.get("retain", 0)
                    delete = delta.get("delete")
                    if delete is not None:
                        layout = self.layout.takeAt(row)
                        while True:
                            item = layout.takeAt(0)
                            if item is None:
                                return
                            item.widget().deleteLater()
                    for cell in delta.get("insert", []):
                        cell_layout = QHBoxLayout()
                        input_widget = QLineEdit()
                        shared_text = cell["text"]
                        input_widget.textEdited.connect(partial(self.my_text_edited, shared_text))
                        input_widget.setText(str(shared_text))
                        cell_layout.addWidget(input_widget)
                        delete_button = QPushButton("Delete cell")
                        delete_button.clicked.connect(partial(self.delete_cell, cell["id"]))
                        cell_layout.addWidget(delete_button)
                        self.layout.addLayout(cell_layout, row)
                        row += 1

    async def start(self):
        room_name = "my_room"
        async with (
            aconnect_ws(f"http://localhost:1234/{room_name}") as websocket,
                WebsocketProvider(self.doc, HttpxWebsocket(websocket, room_name)),
            ):
                await anyio.Event().wait()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = Notebook()
    async_helper = AsyncHelper(widget.start)
    widget.show()

    sys.exit(app.exec())
