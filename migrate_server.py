#!/usr/bin/env python

import asyncio
import websockets
from protocol import app_state_pb2

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send("ACK from server")
        print(list(app_state_pb2.AppState().FromString(message).user_progress))

start_server = websockets.serve(echo, "0.0.0.0", 8765)
print("server launched!")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
