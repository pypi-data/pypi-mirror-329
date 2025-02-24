# WebSocket Vosp

This package provides a quick-access to what is essentially a boiler-plate socket client; manages socket connections, sends requests, and handles responses. 
## Installation

```bash
pip install websocket_vosp

Usage:

from websocket_vosp import SocketClient

client = SocketClient('example.com', 443)
client.connect()
client.send_request("Hello Server")
response = client.receive_response()
print(response)


```