import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from loguru import logger

from compare_with_saved_data import compare_with_saved_data
from curl import cookies, headers
from db_handler import initialize_database, is_file_sent, log_file_sent
from download_tass_preview import download_photo_preview_by_id
from first_enter import first_enter
from send_message_to_telegram import send_telegram_message
from xlsx_tools import XlsxTools
from datetime import datetime


base_dir = Path().home() / 'Library/Mobile Documents/com~apple~CloudDocs/Documents/TASS/Images_on_site'


def get_response_text(work_url):
    response = requests.get(work_url,
                            cookies=cookies,
                            headers=headers,
                            )
    response.raise_for_status()
    return response.text


def get_int_images_number(soup):
    images_online = soup.find('p', id='nb-result', class_='result-counter').text
    logger.info(images_online)
    return int(images_online.split()[0])


def cook_soup(work_url):
    # извлекаю html text

    html = get_response_text(work_url)
    # получаю объект soup
    soup = BeautifulSoup(html, 'lxml')
    return soup





def main(author_name):
    # получаю ссылку в зависимости от имени автора
    work_url = first_enter(author_name).current_url
    # logger.debug(work_url)

    report_file = f'added_images_{author_name.replace("+", "_")}.xlsx'

    initialize_database()  # Убедиться, что база данных существует

    soup = cook_soup(work_url)

    # получаю количество опубликованных снимков
    int_images_number = get_int_images_number(soup)
    # logger.info(int_images_number)

    if compare_with_saved_data(base_dir, int_images_number):


        xlsx_file = XlsxTools(report_file).initialize()

        # получаю количество страниц со снимками
        pages_number = int_images_number // 20 + 1 if int_images_number % 20 != 0 else int_images_number // 20
        # logger.debug(pages_number)
        url = re.sub(r'1$', '', work_url)
        # logger.debug(f'{url = }')
        for page in range(1, pages_number + 1):

            page_url = f"{url}{page}"
            # logger.debug(page_url)
            soup = cook_soup(page_url)
            thumbs_data = soup.find('ul', id="mosaic").find_all('div',
                                                                class_="thumb-content thumb-width thumb-height")

            for thumb in thumbs_data:

                image_id = thumb.find(class_="title").text.strip()
                image_date = thumb.find(class_="date").text.strip()
                image_title = thumb.find('p').text.strip()
                logger.debug(image_id)
                logger.debug(image_date)
                logger.debug(image_title)
                image_caption = thumb.find(class_="thumb-text").text.replace('Валентин Антонов/ТАСС', '').strip()
                image_caption = image_caption.splitlines()[-1].strip()
                # del image_caption[3:6]
                logger.debug(image_caption)
                image_link = thumb.find('img').get('src')
                logger.debug(image_link)

                if not is_file_sent(image_id):
                    log_file_sent(image_id, image_caption, image_link)
                    logger.info(f'{image_id = } added')
                    XlsxTools(report_file).append_data(xlsx_file,
                                                       [int_images_number, image_id, image_date, image_caption,
                                                        image_link])
                    download_photo_preview_by_id(image_id, f'{base_dir}/{datetime.now().strftime("%Y%m%d-%H%M")}', image_file_name=None)
                int_images_number -= 1

    else:
        logger.info("NO NEW IMAGES ADDED")
        send_telegram_message("NO NEW IMAGES ADDED")


#
if __name__ == '__main__':
    author = "Валентин+Антонов"
    # author = "Семен Лиходеев"

    main(author)
