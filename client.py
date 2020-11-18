import asyncio
import websockets
import json

async def hello():
    uri = "ws://localhost:8088"
    async with websockets.connect(uri) as websocket:
        my_dict = {"row": 100}
        await websocket.send(json.dumps(my_dict))
        res = await websocket.recv()
        return res

def get_res_from_socket():
    loop = asyncio.get_event_loop()
    a = loop.run_until_complete(hello())
    loop.close()
    return a

