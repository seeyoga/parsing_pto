import os

from final_csv import read_csv, preformat_data_for_yandex_map, write_final_data_csv
from parsing import get_all_file_dir, get_page, parsing_all_items, write_csv
from web_driver import start_brouser, time, city_search, save_pages_with_pto


def main():
    if not os.path.exists('pages_html'):  # Проверяем существует ли папка pages_html
        os.mkdir('pages_html')

    ### Получаем веб страницы
    driver = start_brouser()
    time.sleep(2)
    driver = city_search('Москва', driver)
    save_pages_with_pto(driver)

    ### Парсим веб страницы и получаем файл с данными
    files = get_all_file_dir('pages_html')
    data_list = []
    for file in files:
        page_html = get_page(file)
        items_list = parsing_all_items(page_html)
        data_list.extend(items_list)

    write_csv('out_data.csv', data_list)

    ### Форматируем файл для загрузки в яндекс карты
    data_list = read_csv('out_data.csv')
    final_list = preformat_data_for_yandex_map(data_list)
    write_final_data_csv('final_data.csv', final_list)


if __name__ == '__main__':
    main()
