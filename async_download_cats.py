import asyncio
from datetime import datetime
from pathlib import Path

import aiofiles
import aiofiles.os
import aiohttp


URL = 'https://api.thecatapi.com/v1/images/search'
BASE_DIR = Path(__file__).parent
CATS_DIR = BASE_DIR / 'cats'


async def get_new_image_url():
    async with aiohttp.ClientSession() as session:
        response = await session.get(URL)
        data = await response.json()
        random_cat = data[0]['url']
        return random_cat


async def download_file(url):
    filename = url.split('/')[-1]
    async with aiohttp.ClientSession() as session:
        result = await session.get(url)
        async with aiofiles.open(CATS_DIR / filename, 'wb') as f:
            await f.write(await result.read())


async def download_new_cat_image():
    url = await get_new_image_url()
    await download_file(url)


async def create_dir(dir_name):
    await aiofiles.os.makedirs(
        dir_name,
        exist_ok=True,
    )


async def main():
    await create_dir(CATS_DIR)
    tasks = [
        asyncio.ensure_future(download_new_cat_image()) for _ in range(100)
    ]
    await asyncio.wait(tasks)


async def list_dir(dir_name):
    files_and_dirs = await aiofiles.os.listdir(dir_name)
    print(*files_and_dirs, sep='\n')


if __name__ == '__main__':
    start_time = datetime.now()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    end_time = datetime.now()
    print(f'Время выполнения программы: {end_time - start_time}.')
    asyncio.run(list_dir(CATS_DIR))
