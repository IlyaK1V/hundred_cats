from datetime import datetime
from pathlib import Path
import asyncio

import aiofiles.os
import aiohttp
import aiofiles

BASE_DIR = Path(__file__).parent
CATS_DIR = BASE_DIR / 'cats'
URL = 'https://api.thecatapi.com/v1/images/search'


# Асинхронная функция для получения нового изображения.


async def get_new_image_url():
    # Создать асинхронную сессию для выполнения HTTP-запроса.
    async with aiohttp.ClientSession() as session:
        # Выполнить асинхронный GET-запрос на указанный URL.
        response = await session.get(URL)
        # Асинхронно получить тело ответа в формате JSON.
        data = await response.json()
        # Извлечь URL случайного изображения из ответа.
        random_cat = data[0]['url']
        # Вернуть URL изображения.
        return random_cat


async def download_file(url):
    filename = url.split('/')[-1]
    async with aiohttp.ClientSession() as session:
        result = await session.get(url)
        # Ранее файлы сохранялся в корневую директорию проекта,
        # но теперь будут сохраняться в директорию, путь к которой
        # хранится в константе CATS_DIR — это директория cats.
        async with aiofiles.open(CATS_DIR / filename, 'wb') as f:
            await f.write(await result.read())


async def download_new_cat_image():
    url = await get_new_image_url()
    await download_file(url)


async def create_dir(dir_name):
    # Асинхронно создать директорию.
    await aiofiles.os.makedirs(
        dir_name,
        exist_ok=True
    )


async def main():
    # Создать список задач для асинхронного выполнения.
    await create_dir('cats')
    tasks = [
        # Асинхронно выполнить функцию get_new_image_url() 100 раз.
        asyncio.ensure_future(download_new_cat_image()) for _ in range(100)
    ]
    # Подождать, пока выполнятся все задачи.
    await asyncio.wait(tasks)


async def list_dir(dir_name):
    # Асинхронно получить список файлов и поддиректорий в указанной директории.
    files_and_dirs = await aiofiles.os.listdir(dir_name)
    # Напечатать каждый элемент содержимого директории,
    # разделяя их переносом строки.
    print(*files_and_dirs, sep='\n')

# Главная асинхронная функция.


# Точка входа в программу.
if __name__ == '__main__':
    # Записать текущее время начала выполнения программы.
    start_time = datetime.now()

    # Получить текущий событийный цикл.
    loop = asyncio.get_event_loop()
    # Запустить основную корутину и подождать, пока она завершится.
    loop.run_until_complete(main())

    # Записать текущее время окончания выполнения программы.
    end_time = datetime.now()
    # Напечатать время выполнения программы.
    print(f'Время выполнения программы: {end_time - start_time}.')
    asyncio.run(list_dir(CATS_DIR))
