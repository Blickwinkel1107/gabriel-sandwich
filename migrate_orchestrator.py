import asyncio
import websockets
import sys

ADDR1 = "cloudlet021.elijah.cs.cmu.edu:8765"
ADDR2 = "128.2.222.34:8765"

async def transfer_state(uri):
    uri = 'ws://%s' % uri
    async with websockets.connect(uri) as websocket:
        await websocket.send("START_MIGRATE")
        recv_msg = await websocket.recv()
        print(recv_msg)
        
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(transfer_state(sys.argv[1]))