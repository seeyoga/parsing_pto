import csv
from settings import logger

filename = 'out_data.csv'


def read_csv(filename):
    with open(filename, 'r') as file:
        data_csv = csv.DictReader(file)
        data_list = [row for row in data_csv]
    logger.info(f'Прочитали данные из файла out_data.csv')
    return data_list


def preformat_data_for_yandex_map(data_list: list):
    """ Функция для подготовки данных к загрузки в яндекс карты """
    final_list = []
    for idx, row in enumerate(data_list):
        item = {
            'latitude': row['latitude'],
            'longitude': row['longitude'],
            'descriptions': f"Статус: {row['is_active']}, Адрес: {row['address']}, Номер телефона: {row['phone']},  Email: {row['email']} ,Сайт: {row['web_site']} ",
            'signature': row['organization'],
            'serial_number': idx + 1
        }
        print(item)
        final_list.append(item)

    return final_list


def write_final_data_csv(filename: str, data: list):
    with open(filename, "a") as file:
        name_colums = ['latitude', 'longitude', 'descriptions', 'signature', 'serial_number']
        writer = csv.DictWriter(file, fieldnames=name_colums)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        logger.info(f'Записали файл для Яндекс карт')
