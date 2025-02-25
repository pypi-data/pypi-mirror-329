from pycrdt import (
    YMessageType,
    create_sync_message,
    create_update_message,
    handle_sync_message,
)


class WebsocketProvider:
    def __init__(self, ydoc, websocket) -> None:
        self._ydoc = ydoc
        self._websocket = websocket
        self._updates = []

    def start(self):
        self._subscription = self._ydoc.observe(lambda event: self._updates.insert(0, event.update))
        sync_message = create_sync_message(self._ydoc)
        self._websocket.send_bytes(sync_message)

    def stop(self):
        self._ydoc.unobserve(self._subscription)

    def run(self):
        while self._updates:
            update = self._updates.pop()
            message = create_update_message(update)
            self._websocket.send_bytes(message)

        try:
            message = bytes(self._websocket.receive_bytes(0))
        except Exception:
            return

        if message[0] == YMessageType.SYNC:
            reply = handle_sync_message(message[1:], self._ydoc)
            if reply is not None:
                self._websocket.send_bytes(reply)
