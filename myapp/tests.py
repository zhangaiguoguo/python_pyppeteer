import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor

thread_pool = ThreadPoolExecutor(max_workers=2)

number = 1


def fn():
    global number
    number += 1
    promise = threading.Event()
    print('hhh -', number)
    print('')
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(fn2(promise))
    except Exception as e:
        print(e)
        asyncio.run(fn2(promise))
    promise.wait()


async def fn2(promise):
    await asyncio.sleep(4)
    promise.set()


# thread_pool.submit(fn)
# print('number - ', number)
# thread_pool.submit(fn)
# print('number - ', number)


# def fff(a, b, **kwargs):
#     print(kwargs)
#
#
# fff(1, 2, c=3, d=4, e=5)
