# OBS-WEBSOCKET-PY

## Events

```py
#!/usr/bin/env python3

import sys
import time

import logging
logging.basicConfig(level=logging.DEBUG)

sys.path.append('../')
from obswebsocket import obsws, events  # noqa: E402

host = "localhost"
port = 4455
password = "secret"


def on_event(message):
    print("Got message: {}".format(message))


def on_switch(message):
    print("You changed the scene to {}".format(message.getSceneName()))


ws = obsws(host, port, password)
ws.register(on_event)
ws.register(on_switch, events.SwitchScenes)
ws.register(on_switch, events.CurrentProgramSceneChanged)
ws.connect()

try:
    print("OK")
    time.sleep(10)
    print("END")

except KeyboardInterrupt:
    pass

ws.disconnect()
```

## Reconnect

```py
#!/usr/bin/env python3

import sys
import time

import logging
logging.basicConfig(level=logging.DEBUG)

sys.path.append('../')
from obswebsocket import obsws  # noqa: E402

host = "localhost"
port = 4455
password = "secret"


def on_connect(obs):
    print("on_connect({})".format(obs))


def on_disconnect(obs):
    print("on_disconnect({})".format(obs))


ws = obsws(host, port, password, authreconnect=1, on_connect=on_connect, on_disconnect=on_disconnect)
ws.connect()

try:
    print("Running. Now try to start/quit obs multiple times!")
    time.sleep(30)
    print("End of test.")

except KeyboardInterrupt:
    pass

ws.disconnect()
```

## Switch Scenes

```py
#!/usr/bin/env python3

import sys
import time

import logging
logging.basicConfig(level=logging.DEBUG)

sys.path.append('../')
from obswebsocket import obsws, requests  # noqa: E402

host = "localhost"
port = 4455
password = "secret"

ws = obsws(host, port, password)
ws.connect()

try:
    scenes = ws.call(requests.GetSceneList())
    for s in scenes.getScenes():
        name = s['sceneName']
        print("Switching to {}".format(name))
        ws.call(requests.SetCurrentProgramScene(sceneName=name))
        time.sleep(2)

    print("End of list")

except KeyboardInterrupt:
    pass

ws.disconnect()
```

## Usage

_Output of `pydoc obswebsocket.core.obsws`_

```bash
Help on class obsws in obswebsocket.core:

obswebsocket.core.obsws = class obsws
 |  Core class for using obs-websocket-py
 |
 |  Simple usage: (v5 api)
 |      >>> from obswebsocket import obsws, requests
 |      >>> client = obsws("localhost", 4455, "secret")
 |      >>> client.connect()
 |      >>> client.call(requests.GetVersion()).getObsVersion()
 |      '29.0.0'
 |      >>> client.disconnect()
 |
 |  Methods defined here:
 |
 |  __init__(self, host='localhost', port=4444, password='', legacy=None, timeout=60, authreconnect=0, on_connect=None, on_disconnect=None)
 |      Construct a new obsws wrapper
 |
 |      :param host: Hostname to connect to
 |      :param port: TCP Port to connect to (Default is 4444)
 |      :param password: Password for the websocket server (Leave this field empty if auth is not enabled)
 |      :param legacy: Server is using old obs-websocket protocol (v4). Default is v5 (False) except if port is 4444.
 |      :param timeout: How much seconds to wait for an answer after sending a request.
 |      :param authreconnect: Try to reconnect if websocket is closed, value is number of seconds between attemps.
 |      :param on_connect: Function to call after successful connect, with parameter (obsws)
 |      :param on_disconnect: Function to call after successful disconnect, with parameter (obsws)
 |
 |  call(self, obj)
 |      Make a call to the OBS server through the Websocket.
 |
 |      :param obj: Request (class from obswebsocket.requests module) to send
 |          to the server.
 |      :return: Request object populated with response data.
 |
 |  connect(self)
 |      Connect to the websocket server
 |
 |      :return: Nothing
 |
 |  disconnect(self)
 |      Disconnect from websocket server
 |
 |      :return: Nothing
 |
 |  reconnect(self)
 |      Restart the connection to the websocket server
 |
 |      :return: Nothing
 |
 |  register(self, func, event=None)
 |      Register a new hook in the websocket client
 |
 |      :param func: Callback function pointer for the hook
 |      :param event: Event (class from obswebsocket.events module) to trigger
 |          the hook on. Default is None, which means trigger on all events.
 |      :return: Nothing
 |
 |  unregister(self, func, event=None)
 |      Unregister a new hook in the websocket client
 |
 |      :param func: Callback function pointer for the hook
 |      :param event: Event (class from obswebsocket.events module) which
 |          triggered the hook on. Default is None, which means unregister this
 |          function for all events.
 |      :return: Nothing
```

---

## Tests

```py
from unittest.mock import patch, Mock
from queue import Queue, Empty
import time

from obswebsocket import obsws, requests, events


def fake_send(data):
    if data == '{"request-type": "GetAuthRequired", "message-id": "1"}':
        fake_recv.queue.put('{"status":"ok"}')
    elif data == '{"message-id": "2", "request-type": "FakeRequest"}':
        fake_recv.queue.put('{"message-id": "2", "status":"ok"}')
    elif data == '{"op": 1, "d": {"rpcVersion": 1, "authentication": "", "eventSubscriptions": 1023}}':
        fake_recv.queue.put('{"op": 2, "d": {"negotiatedRpcVersion": 1 }}')
    elif data == '{"op": 6, "d": {"requestId": "1", "requestType": "FakeRequest", "requestData": {}}}':
        fake_recv.queue.put('{"op": 7, "d": {"requestId": "1", "requestType": "FakeRequest", "requestStatus": {"result": true, "code": 100}}}')
    else:
        raise Exception(data)


def fake_recv():
    try:
        return fake_recv.queue.get(timeout=1)
    except Empty:
        return ""
fake_recv.queue = Queue()   # noqa: E305


def test_request():
    ws = obsws("127.0.0.1", 4455, "")
    with patch('websocket.WebSocket') as mock:
        mockws = mock.return_value
        mockws.send = Mock(wraps=fake_send)
        mockws.recv = Mock(wraps=fake_recv)

        fake_recv.queue.put('{"op": 0, "d": { "obsWebSocketVersion": "fake", "rpcVersion": 1 }}')
        ws.connect()
        mockws.connect.assert_called_once_with("ws://127.0.0.1:4455")
        assert ws.thread_recv.running

        r = ws.call(requests.FakeRequest())
        assert r.name == "FakeRequest"
        assert r.status

        ws.disconnect()
        assert not ws.thread_recv


def test_event():
    ws = obsws("127.0.0.1", 4455, "")
    with patch('websocket.WebSocket') as mock:
        mockws = mock.return_value
        mockws.send = Mock(wraps=fake_send)
        mockws.recv = Mock(wraps=fake_recv)

        fake_recv.queue.put('{"op": 0, "d": { "obsWebSocketVersion": "fake", "rpcVersion": 1 }}')
        ws.connect()
        mockws.connect.assert_called_once_with("ws://127.0.0.1:4455")
        assert ws.thread_recv.running

        def on_fake_event(message):
            assert message.name == "FakeEvent"
            assert message.getFakeKey() == "fakeValue"
            on_fake_event.ok = True

        on_fake_event.ok = False
        ws.register(on_fake_event, events.FakeEvent)
        fake_recv.queue.put('{"op": 5, "d": { "eventType": "FakeEvent", "eventIntent": 1, "eventData": { "fakeKey": "fakeValue" }}}')
        time.sleep(1)
        assert on_fake_event.ok

        ws.disconnect()
        assert not ws.thread_recv
```
