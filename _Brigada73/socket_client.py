import websocket
import json
from threading import Thread, Event


class SOCKET:
    def __init__(self, token,sessionid,user):

        self.user = user
        self.connection_event = Event()
        self.ws = websocket.WebSocketApp("ws://127.0.0.1:8002/ws/order/",
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
        print('message:', message)
        data = json.loads(message)
        print("pyOrderSocket onmessage")
        print(data)

    def on_open(self, *args, **kwargs):
        print("pyOrderSocket connection established.")
        # data = {"type": "user_id", 'user_id': self.user.id}
        # self.ws.send(json.dumps(data))
        self.connection_event.set()

    def on_close(self, *args, **kwargs):
        print("pyOrderSocket connection closed.")

    def send_notify(self, message,type):
        data = {"type": type, "message": message, 'user_id': self.user.id}
        self.ws.send(json.dumps(data))

    def on_error(self, error, *args, **kwargs):
        print("pyError on pysocket:", error)
