#!/usr/bin/env python

import logging
import asyncio
import websockets
from multiprocessing import Queue
import sys
from .protocol import app_state_pb2

# ADDRESS = "localhost"
MIGRATE_ADDRESS = "cloudlet021.elijah.cs.cmu.edu"
MIGRATION_PORT = 8765

extract_state_func = lambda : bytes(0)
app_in_queue:Queue
logger = logging.getLogger(__name__)

def register_app_in_queue(queue):
    global app_in_queue
    app_in_queue = queue

def register_extract_state_api(func):
    global extract_state_func
    extract_state_func = func

async def send_state():
    global app_in_queue
    state = extract_state_func()
    logger.info("send state info: %s" % list(app_state_pb2.AppState().FromString(state).user_progress))
    uri = 'ws://%s:%d' % (MIGRATE_ADDRESS, MIGRATION_PORT)
    async with websockets.connect(uri) as websocket:
        await websocket.send(state)
        recv_msg = await websocket.recv()
        logger.info('recv_msg: %s' % recv_msg)
        app_in_queue.put_nowait("MIGRATE_FINISHED".encode('utf-8'))