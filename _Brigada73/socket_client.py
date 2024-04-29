import websocket
import json
from threading import Thread, Event


class SOCKET:
    def __init__(self, url, request):
        user = request.user
        token = request.COOKIES.get('csrftoken')
        sessionid = request.COOKIES.get('sessionid')
        self.user_id = user.id
        self.connection_event = Event()

        self.ws = websocket.WebSocketApp(url,
                                         on_message=self.on_message,
                                         on_open=self.on_open,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         header={'Cookies': f'csrftoken={token}; sessionid={sessionid}'},
                                         cookie=f'csrftoken={token}, sessionid={sessionid}',
                                         )

    def connect(self):
        Thread(target=self.ws.run_forever, kwargs={"ping_interval": 3540, "ping_timeout": 5}, daemon=True).start()
        self.connection_event.wait()

    def on_message(self, message, *args, **kwargs):
        print("py client message", json.loads(message))

    def on_open(self, *args, **kwargs):
        print("py client open")
        self.connection_event.set()

    def on_close(self, *args, **kwargs):
        print("py client closed")

    def send_notify(self, message, notify_type):
        data = {"type": notify_type, "message": message, 'user_id': self.user_id}
        self.ws.send(json.dumps(data))

    def on_error(self, error, *args, **kwargs):
        print("py client error:", error)
