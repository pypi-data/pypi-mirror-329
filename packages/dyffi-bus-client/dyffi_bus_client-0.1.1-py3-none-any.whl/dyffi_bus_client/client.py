import requests
import json
import threading
import time

from websocket import create_connection, WebSocketConnectionClosedException


class DyffiBusClient:
    def __init__(self, api_url):
        self.api_url = api_url.rstrip('/')

    def publish(self, topic, payload):
        url = f"{self.api_url}/publish"
        data = {"topic": topic, "payload": payload}
        print(url)
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("message_id")

    def subscribe(self, topic, handler, blocking=False):
        if blocking:
            self._subscribe_thread(topic, handler)
        else:
            thread = threading.Thread(target=self._subscribe_thread, args=(topic, handler), daemon=True)
            thread.start()

    def _subscribe_thread(self, topic, handler):
        ws_url = self.api_url.replace("http", "ws") + f"/ws/{topic}"
        try:
            ws = create_connection(ws_url)
            while True:
                message_json = ws.recv()
                message = json.loads(message_json)
                handler(message)
        except WebSocketConnectionClosedException:
            print("WebSocket соединение закрыто.")
        except Exception as e:
            print(f"Ошибка в подписке: {e}")

    def listen(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Выход из прослушивания.")
