import asyncio

async def func_normal():
    print('A')
    await asyncio.sleep(5)
    print('B')
    return 'saad'

async def func_infinite():
    for i in range(10):
        print("--%d" % i)
    return 'saad2'

loop = asyncio.get_event_loop()
tasks = func_normal(), func_infinite()
a, b = loop.run_until_complete(asyncio.gather(*tasks))
print("func_normal()={a}, func_infinite()={b}".format(**vars()))
loop.close()