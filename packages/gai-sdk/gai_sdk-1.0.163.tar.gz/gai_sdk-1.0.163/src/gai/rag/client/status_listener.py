import asyncio
import websockets
import os
from gai.lib.logging import getLogger
logger = getLogger(__name__)

'''
This is class is used by the client-side websocket to receive status updates from the server.
'''

class StatusListener:

    def __init__(self, ws_url):
        self.ws_url = ws_url

    async def listen(self, async_callback):
        async with websockets.connect(self.ws_url) as websocket:
            logger.info(f"Connected to {self.ws_url}")
            while True:
                try:
                    message = await websocket.recv()
                    logger.debug(f"StatusListener.listen: Client-side received from websocket {message}")                    
                    await async_callback(message)
                    # await asyncio.sleep(0)
                    # asyncio.create_task(callback(message))
                except websockets.ConnectionClosedError:
                    logger.warn("StatusListener.listen: Server disconnected.")
                    break
                except Exception as e:
                    logger.error(f"Error: {e}")
                    raise e
    
        