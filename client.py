import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8088"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello world from Python!")
        res = await websocket.recv()
        return res

def get_res_from_socket():
    loop = asyncio.get_event_loop()
    a = loop.run_until_complete(hello())
    # print(a)
    loop.close()
    return a

