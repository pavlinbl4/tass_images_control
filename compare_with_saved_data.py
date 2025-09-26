from loguru import logger

from send_message_to_telegram import send_telegram_message

"""Если переданное в функцию число не равно числу в текстовом файле,
то функция возвращает True"""


def compare_with_saved_data(base_dir, int_images_number):
    with open(
            f'{base_dir}/images_on_site.txt',
            'r+') as text_file:
        digit_in_file = int(text_file.read().strip())
        logger.info(f'{digit_in_file = }')
        logger.info(f'{int_images_number = }')

        if digit_in_file != int_images_number:
            logger.info(f'добавленно {int_images_number - digit_in_file} снимка')
            send_telegram_message(f'добавленно {int_images_number - digit_in_file} снимка')
            text_file.seek(0)
            text_file.write(str(int_images_number))
            text_file.truncate()
            return True
        return False
