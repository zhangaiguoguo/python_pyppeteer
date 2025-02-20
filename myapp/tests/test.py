import aiohttp
import asyncio
import json


async def fetch(url, json_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data) as response:
            return await response.text()


async def main():
    url = "http://127.0.0.1:8000/api/cyapp/generate/hiprint/template/toPdf/"
    with open("./data.json", "rb") as ff:
        json_str = json.loads(ff.read().decode("utf-8"))

    # 使用 asyncio.gather 并发执行多个 fetch 调用
    results = await asyncio.gather(
        fetch(url, json_str),
        fetch(url, json_str),
        fetch(url, json_str)
    )
    # 打印结果
    for result in results:
        print(result[0])


# 运行异步主函数
# asyncio.run(main())
