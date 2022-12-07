#!/usr/bin/env python

import logging
import asyncio
from multiprocessing import Queue
import websockets
import sys
from .protocol import app_state_pb2
# from protocol import app_state_pb2
import logging

ADDRESS = "0.0.0.0"
MIGRATION_PORT = 8765

logger = logging.getLogger(__name__)

class MigrateEngine:
    def __init__(self, app_in_queue: Queue):
        self.app_in_queue = app_in_queue
    
    async def handle(self, websocket, _):
        async for message in websocket:
            if message == 'START_MIGRATE':
                await websocket.send("AZURE VM ACKed START_MIGRATE")
                self.app_in_queue.put_nowait("START_MIGRATE".encode('utf-8'))
                continue
            await websocket.send("AZURE VM ACKed app_state")
            app_state = app_state_pb2.AppState().FromString(message)
            user_progress = list(app_state.user_progress)
            logger.info("received remote user_progress: %s" % user_progress)
            self.app_in_queue.put_nowait('MERGE_STATE'.encode('utf-8'))
            self.app_in_queue.put_nowait(message)
            
    def launch(self):
        logger.info("MigrateEngine Launched")
        start_server = websockets.serve(self.handle, ADDRESS, MIGRATION_PORT)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
        
# if __name__ == "__main__":
#     engine = MigrateEngine()
#     engine.launch()