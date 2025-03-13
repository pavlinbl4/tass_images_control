
"""Если переданное в функцию число не равно числу в текстовом файле,
то функция возвращает True"""
def compare_with_saved_data(base_dir, int_images_number):
    with open(
            f'{base_dir}/images_on_site.txt',
            'r+') as text_file:
        if text_file.read().strip() != str(int_images_number):
            text_file.seek(0)
            text_file.write(str(int_images_number))
            text_file.truncate()
            return True
        return False
