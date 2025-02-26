from collections import defaultdict
import json
import logging
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Tuple
from websocket import WebSocketApp
import threading

from desk.types import Subscription, WsMessage

ActiveSubscription = NamedTuple("ActiveSubscription", [("callback", Callable[[Any], None]), ("subscription_id", int)])

class WebSocketManager(threading.Thread):
    def __init__(self, ws_url: str):
        super().__init__()
        self.subscription_id_counter = 0
        self.ws_ready = False
        self.url = ws_url

        self.queued_subscriptions: List[Tuple[Subscription, ActiveSubscription]] = []
        self.active_subscriptions: Dict[str, List[ActiveSubscription]] = defaultdict(list)

        self.ws = WebSocketApp(ws_url, on_message=self.on_message, on_open=self.on_open)

        self.stop_event = threading.Event()
    
    def run(self):
        self.ws.run_forever(suppress_origin=True, reconnect=1)

    def stop(self):
        self.stop_event.set()
        self.ws.close()

    def on_message(self, _ws, message):
        if message == "Websocket connection established.":
            logging.debug(message)
            return
        ws_msg: WsMessage = json.loads(message)

        identifier = ws_msg['type']
        if identifier is None:
            logging.debug("Websocket not handling empty message")
            return
        active_subscriptions = self.active_subscriptions[identifier]
        if len(active_subscriptions) == 0:
            print("Websocket message from an unexpected subscription:", message, identifier)
        else:
            for active_subscription in active_subscriptions:
                active_subscription.callback(ws_msg)

    def on_open(self, _ws):
        logging.debug("on_open")
        self.ws_ready = True
        for subscription, active_subscription in self.queued_subscriptions:
            self.subscribe(subscription, active_subscription.callback, active_subscription.subscription_id)

    def subscribe(
        self, subscription: Subscription, callback: Callable[[Any], None], subscription_id: Optional[int] = None
    ) -> int:
        if subscription_id is None:
            self.subscription_id_counter += 1
            subscription_id = self.subscription_id_counter
        if not self.ws_ready:
            logging.debug("enqueueing subscription")
            self.queued_subscriptions.append((subscription, ActiveSubscription(callback, subscription_id)))
        else:
            logging.debug("subscribing")
            identifier = subscription['type']
            self.active_subscriptions[identifier].append(ActiveSubscription(callback, subscription_id))
            self.ws.send(json.dumps({"method": "subscribe", "subscription": subscription}))