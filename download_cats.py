import os
from datetime import datetime
from pathlib import Path

import requests

BASE_DIR = Path(__file__).parent
URL = 'https://api.thecatapi.com/v1/images/search'
CATS_DIR = BASE_DIR / 'cats'


def get_new_image_url():
    # Отправить GET-запрос и получить JSON-ответ от API.
    response = requests.get(URL).json()
    # Извлечь URL нулевого элемента списка из ответа.
    random_cat = response[0].get('url')
    # Вернуть URL изображения.
    return random_cat


def download_file(url):
    # Получить имя файла из URL: разделить строку по символу '/' 
    # и взять последний элемент.
    # Например, из 'http://example.com/file.txt' будет получено 'file.txt'.
    filename = url.split('/')[-1]
    
    # Отправить GET-запрос по указанному URL и получить ответ.
    response = requests.get(url)
    
    # Открыть файл для записи в двоичном режиме 
    # в указанной директории CATS_DIR
    # и записать содержимое ответа в файл.
    with open(CATS_DIR / filename, 'wb') as file:
        file.write(response.content)


def download_new_cat_image():
    # Получить URL нового изображения, вызвав функцию get_new_image_url().
    url = get_new_image_url()
    # Скачать файл-картинку по полученному URL, вызвав функцию download_file().
    download_file(url)


def create_dir(dir_name):
    # Создать директорию, если она не существует.
    os.makedirs(dir_name, exist_ok=True)


def list_dir(dir_name):
    # Вывести содержимое директории, переданной в качестве аргумента dir_name.
    print(
        # Получить список файлов и папок в указанной директории.
        *os.listdir(dir_name),
        # Вывести каждый элемент списка на новой строке.
        sep='\n'
    )


def main():
    # Создать директорию CATS_DIR, если она ещё не существует.
    create_dir(CATS_DIR)
    
    # Запустить цикл, который повторяется 100 раз.
    for _ in range(100):
        # Скачать новое изображение и сохранить его в CATS_DIR.
        download_new_cat_image()


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print(f'Время выполнения программы: {end_time - start_time}.')
    list_dir(CATS_DIR)
