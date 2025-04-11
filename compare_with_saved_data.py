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
        # if text_file.read().strip() != str(int_images_number):
        if digit_in_file != int_images_number:

            logger.info(f'добавленно {int_images_number - digit_in_file} снимка')
            send_telegram_message(f'добавленно {int_images_number - digit_in_file} снимка')
            text_file.seek(0)
            text_file.write(str(int_images_number))
            text_file.truncate()
            return True
        return False

class CompareWithSavedData:
    def __init__(self, base_dir, text_file_name, any_date):
        self.base_dir = base_dir
        self.any_date = any_date
        self.text_file_name = text_file_name

    def compare(self):
        with open(self.text_file_name, 'r+') as text_file:
            file_content = text_file.read().strip()  # Сохраняем значение один раз
            logger.info(f'{file_content = }')
            logger.info(f'{self.any_date = }')
            logger.info(file_content != str(self.any_date))
            if file_content != str(self.any_date):
                text_file.seek(0)
                text_file.write(str(self.any_date))
                text_file.truncate()
                return True
            return False

