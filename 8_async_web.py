import requests
import asyncio
from time import time

import aiohttp


URL = 'https://loremflickr.com/320/240'

def get_file(url):
    r = requests.get(url, allow_redirects=True)
    return r

# r = get_file(url)
# print(r)

def write_file(response):
    filename = response.url.split('/')[-1]
    with open(filename, 'wb') as file:
        file.write(response.content)

def main():
    t0 = time()
    for i in range(10):
        write_file(get_file(URL))
    print(time() - t0)



# exaple 2 aiohttp

def write_image(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        write_image(data, f'{i}.jpeg')
        # print(data)


async def main2():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task(fetch_content(URL, session))
            tasks.append(task)

        await asyncio.gather(*task)


if __name__ == '__main__':
    # main()
    t0 = time()
    asyncio.run(main2())
    print(time() - t0)


