import asyncio
import websockets
from protocol import app_state_pb2
import sys


ADDRESS = "localhost"
MIGRATION_PORT = 8765
arr = ['START', 'NOTHING', 'BREAD', 'CUCUMBER', 'BREAD', 'LETTUCE']

async def send_state():
    uri = 'ws://%s:%d' % (ADDRESS, MIGRATION_PORT)
    app_state = app_state_pb2.AppState()
    app_state.user_progress.extend(arr)
    print(app_state)
    async with websockets.connect(uri) as websocket:
        await websocket.send(app_state.SerializeToString())
        recv_msg = await websocket.recv()
        print(recv_msg)
        
async def send_state_by_uri(uri):
    uri = 'ws://%s' % uri
    app_state = app_state_pb2.AppState()
    app_state.user_progress.extend(arr)
    # print(app_state)
    async with websockets.connect(uri) as websocket:
        print("sent app state: %s" % arr)
        await websocket.send(app_state.SerializeToString())
        recv_msg = await websocket.recv()
        print(recv_msg)
        
async def transfer_state(uri):
    uri = 'ws://%s' % uri
    async with websockets.connect(uri) as websocket:
        await websocket.send("START_MIGRATE")
        recv_msg = await websocket.recv()
        print(recv_msg)
        
if __name__ == "__main__":
    # asyncio.get_event_loop().run_until_complete(send_state())
    # asyncio.get_event_loop().run_until_complete(send_state_by_uri(sys.argv[1]))
    asyncio.get_event_loop().run_until_complete(transfer_state(sys.argv[1]))