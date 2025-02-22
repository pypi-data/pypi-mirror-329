import logging
import threading
import time

import websocket

from maitai_common.processes.io_thread import IOThread

logging.getLogger("websocket").setLevel(logging.FATAL)


class WebsocketListenerThread(IOThread):
    def __init__(self, path, type, key=None, interval=60):
        super(WebsocketListenerThread, self).__init__(interval=interval)
        self.child_name = f"{self.__class__.__name__}"
        self.messages = []
        self.ws_url = f"{path}?type={type}"
        if key:
            self.ws_url += f"&key={key}"
        self.ws = None
        self.ws_thread = None  # Single thread reference
        self.closing_ws = False
        self.connection_established_event = threading.Event()
        self.retry_backoff = 1
        self.connection_lock = threading.Lock()

    def connect_to_websocket(self):
        self.connection_established_event.clear()
        with self.connection_lock:
            # Only create new connection if we're still running
            if self.run_thread and not self.closing_ws:
                old_ws = self.ws
                self.ws = websocket.WebSocketApp(
                    self.ws_url,
                    on_message=self.on_message,
                    on_close=self.on_close,
                    on_error=self.on_error,
                    on_open=self.on_open,
                )
                if self.ws_thread and self.ws_thread.is_alive():
                    old_ws_thread = self.ws_thread
                    self.ws_thread = None
                    old_ws_thread.join(timeout=2.0)
                # Create and start new thread
                self.ws_thread = threading.Thread(
                    target=self.ws.run_forever, name="WebsocketThread", daemon=True
                )
                self.ws_thread.start()
                self.retry_backoff = 1
                if old_ws:
                    old_ws.close()

    def on_message(self, ws, message):
        self.messages.append(message)

    def on_close(self, ws, _, __):
        if self.run_thread and not self.closing_ws:
            self.connect_to_websocket()

    def on_open(self, ws):
        self.connection_established_event.set()  # Set the event when connection is open
        if not self.run_thread or self.closing_ws:
            ws.close()
            if self.ws:
                self.ws.close()

    def on_error(self, ws, error):
        time.sleep(self.retry_backoff)
        self.retry_backoff *= 2
        self.retry_backoff = min(self.retry_backoff, 10)
        self.connect_to_websocket()

    def initialize(self):
        self.connect_to_websocket()

        super(WebsocketListenerThread, self).initialize()

    def terminate(self):
        self.closing_ws = True
        if self.ws:
            self.ws.close()

        # Join the single thread with timeout
        if self.ws_thread and self.ws_thread.is_alive():
            self.ws_thread.join(timeout=2.0)

        self.ws_thread = None
        super(WebsocketListenerThread, self).terminate()

    def clear(self):
        self.messages = []

    def process(self):
        if self.run_thread:
            # Check if websocket is connected and functioning
            if not self.ws or not self.ws.sock or not self.ws.sock.connected:
                old_ws = self.ws
                # Temporarily override the on_close to prevent reconnection
                old_on_close = old_ws.on_close
                old_ws.on_close = lambda *args, **kwargs: None

                try:
                    # Try to establish a new connection
                    self.connect_to_websocket()
                    # Wait for the on_open callback to set the event
                    self.connection_established_event.wait()
                    # If successful, close the old connection
                    old_ws.close()
                except Exception as e:
                    # If new connection fails, keep the old connection
                    old_ws.on_close = old_on_close
                    self.ws = old_ws

        super(WebsocketListenerThread, self).process()
