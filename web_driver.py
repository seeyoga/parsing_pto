import random
from settings import logger
from selenium import webdriver
import time


def start_brouser():
    """ Функция для запуска браузера """
    driver = webdriver.Firefox(executable_path='driver/geckodriver')
    driver.get("https://oto-register.autoins.ru/oto/")
    logger.info(f'Открыли браузер')
    return driver


def city_search(city: str, driver):
    ''' Функция для получения операторов технического осмотра по городу '''
    driver.find_element_by_xpath('/html/body/form/div[1]/section/div/div[1]/div[2]/input[4]').send_keys(city)
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/form/div[1]/section/div/div[1]/div[3]/input[1]').click()
    logger.info(f'От фильтровали ПТО')
    return driver


def save_html(page, content) -> None:
    """ Функция для сохранения HTML страницы """
    with open(f'pages_html/webpage{page.text}.html', 'w') as f:
        f.write(content)
        logger.info(f'Сохранили страницу {page.text}')


def save_pages_with_pto(driver) -> None:
    """ Функция дял получения страниц и переключения пагинации """
    try:

        total_pages = driver.find_element_by_class_name('modern-page-navigation').find_elements_by_tag_name(
            'a')  # получаем общее число страниц
        number_last_pages = int(total_pages[-2].text)  # берем пред последнее зачение
        for row in range(0, number_last_pages + 1):
            next_page = driver.find_element_by_class_name('modern-page-navigation').find_elements_by_tag_name('a')
            if row == 1:
                next_page[0].click()
            elif row == 2:
                next_page[2].click()
            elif row == 3:
                next_page[3].click()
            elif row == 4:
                next_page[4].click()
            elif row >= 5:
                next_page[5].click()

            page = driver.find_element_by_class_name('modern-page-navigation').find_element_by_class_name(
                'modern-page-current')
            save_html(page, driver.page_source)
            time.sleep(random.randint(3, 8))
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
