import time
from settings import logger, GOOGLE_API_KEY
from bs4 import BeautifulSoup
import csv

from geocoder import geocoder


def get_all_file_dir(folder: str) -> list:
    """ Функция которая возвращает список файлов в папке """
    import os
    filename = [files for _, _, files in os.walk(folder)]
    return sorted(filename[0])


def parsing_item_page(row) -> dict:
    """ Функция для парсинга карточек ОПТ """
    item = {
        'is_active': '',
        'number': '',
        'organization': '',
        'address': '',
        'phone': '',
        'email': '',
        'web_site': ''
    }
    items = row.find_all('td')
    if len(items[3].text.split(',')) > 2:
        item['is_active'] = items[0].find('a').find('div', class_='status')['title']
        item['number'] = items[1].text
        item['organization'] = items[2].text
        item['address'] = items[3].text
        item['phone'] = items[4].text
        item['email'] = items[5].text
        item['web_site'] = items[6].text.replace(';', ',')
        data_gps = geocoder(item['address'], GOOGLE_API_KEY)
        item['latitude'] = data_gps[0]
        item['longitude'] = data_gps[1]
        time.sleep(1)
        return item
    else:
        return None


def get_page(file):
    """ Функция для сбора всех карточек с одной  """
    with open(f'pages_html/{file}', 'r') as file_html:
        data_html = file_html.read()
        soup = BeautifulSoup(data_html, 'lxml')
        pto_table = soup.find("div", class_='registry-table')
        logger.info(f'парсим страницу {file}')
        return pto_table.find_all("tr")


def parsing_all_items(pto_items):
    """ Функция парсит страницу и собирает данные в словарь """
    items_list = []
    for row in pto_items[1::]:
        item = parsing_item_page(row)
        if item is not None:
            items_list.append(item)

    return items_list


def write_csv(filename: str, data: list):
    with open(filename, "a") as file:
        name_colums = ['is_active', 'number', 'organization', 'address', 'phone', 'email', 'web_site', 'latitude',
                       'longitude']
        writer = csv.DictWriter(file, fieldnames=name_colums)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        logger.info(f'Записали файл с ПТО')
